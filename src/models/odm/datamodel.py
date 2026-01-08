from pydantic import BaseModel, ValidationError, Field, ConfigDict
from typing import Optional, ClassVar, Type, List, Any, Dict
from ravendb import DocumentStore

from datetime import datetime, timezone


class DataModel(BaseModel):
    """
    Mongoose-like base model for RavenDB:
      - schema validation (Pydantic)
      - CRUD operations
      - collection auto-naming
      - JSON serialization
    """

    # fields for every datamodel
    Id: Optional[str] = Field(default=None) #for ravendDB match
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = False

    # Class-level RavenDB store
    _store: Optional[DocumentStore] = None 
    model_config =ConfigDict(
        arbitrary_types_allowed = True
    )

    def __hash__(self):
        # Hash using 'id' if available, otherwise use object id
        return hash(self.Id or id(self))
   
    #Create/Update
    async def save(self, session):
        if not session:
            raise RuntimeError("Session not set in model")
        
        try:
            session.store(self)
            session.save_changes()
        except ValidationError as e:
            print("Validation",e)
            return self    
        # Guarantee ID exists after save
        if not self.Id:
            raise ValueError("RavenDB did not generate an ID for this document.")
        return self

    # Soft delete method
    def delete(self, session):
        self.is_deleted = True
        session.store(self)
        session.save_changes()

    # Restore method
    def restore(self, session):
        self.is_deleted = False
        session.store(self)
        session.save_changes()
        return self
    
    @classmethod
    def connect_to_store(cls, store: Any):
        cls._store = store

    #Find By Id    
    @classmethod
    async def find_by_id(cls: Type["DataModel"],session, doc_id: str) -> Optional["DataModel"]:
        data=None
        try:
            data = session.load(doc_id, cls)
            if data and data.is_deleted:
                data = None 
        except ValidationError as e:
            print("Validation",e)     
        return data
        
    #Find all non-deleted
    @classmethod
    def find_active(cls: Type["DataModel"], state: Dict):
        collection_name = state.dbstore.conventions.get_collection_name(cls)
        return state.dbsession.query_collection(collection_name).where_equals("is_deleted", False)

    #find all for performance comparisons!
    @classmethod
    def find_all(cls: Type["DataModel"], state: Dict):
        collection_name = state.dbstore.conventions.get_collection_name(cls)
        return state.dbsession.query_collection(collection_name)

    #Raq Rql support
    @classmethod
    def raw_rql(cls: Type["DataModel"], session, query: str) -> List["DataModel"]:

        # Execute the raw query
        results = list(session.advanced.raw_query(query, object_type=cls))
        return results
