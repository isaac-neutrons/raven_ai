from pydantic import BaseModel, ValidationError, Field
from typing import Optional, ClassVar, Type, List, Any, Dict
from ravendb import DocumentStore

import datetime

# RavenDB store (set from your app)
store: Optional[DocumentStore] = None


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
    created_at: datetime = datetime.datetime.now(datetime.UTC).isoformat()
    is_deleted: bool = False

    # Class-level RavenDB store
    _store: Optional[Any] = None 
    class Config:
        arbitrary_types_allowed = True


    def __hash__(self):
        # Hash using 'id' if available, otherwise use object id
        return hash(self.Id or id(self))
    # ---------------------------
    # CRUD
    # ---------------------------

    async def save(self, session):
        print("fff",self.model_dump(exclude={"session"}))
        if not session:
            raise RuntimeError("Session not set in model")
        
        try:
            session.store(self)
            session.save_changes()
        except ValidationError as e:
            print("Validation",e)    
        # Guarantee ID exists after save
        if not self.Id:
            raise ValueError("RavenDB did not generate an ID for this document.")
        print("self",self)
        return self

    # Soft delete method
    def delete(self):
        self.is_deleted = True
        self.save()

    # Restore method
    def restore(self):
        self.is_deleted = False
        self.save()

    @classmethod
    def connect_to_store(cls, store: Any):
        cls._store = store
        
    @classmethod
    def find_by_id(cls: Type["DataModel"], doc_id: str) -> Optional["DataModel"]:
        if store is None:
            raise RuntimeError("Raven store not initialized.")

        with store.open_session() as session:
            data = session.load(doc_id)
            if data:
                return cls(**data)
            return None

    @classmethod
    def find(cls: Type["DataModel"], **filters) -> List["DataModel"]:
        if store is None:
            raise RuntimeError("Raven store not initialized.")

        with store.open_session() as session:
            q = session.query(
                object_type=dict,
                collection_name=cls.collection(),
                is_deleted=False
            )

            for field, value in filters.items():
                q = q.where_equals(field, value)

            docs = list(q)
            return [cls(**d) for d in docs]

    # @classmethod
    # def find_one(cls: Type["DataModel"], **filters) -> Optional["DataModel"]:
    #     results = cls.find(**filters)
    #     return results[0] if results else None
    
    # -------------------------------------------------------
    # RQL SUPPORT
    # -------------------------------------------------------
    @classmethod
    def rql_raw(cls, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Run raw RQL and return raw dicts.
        """
        if store is None:
            raise RuntimeError("Raven store not initialized.")

        with store.open_session() as session:
            q = session.advanced.raw_query(query, dict)

            if params:
                for key, value in params.items():
                    q.add_parameter(key, value)

            return list(q)  # raw list[dict]

    @classmethod
    def rql(cls: Type["DataModel"], query: str, params: Dict[str, Any] = None) -> List["DataModel"]:
        """
        Run raw RQL and return typed Pydantic models.
        """
        raw = cls.rql_raw(query, params)
        return [cls(**doc) for doc in raw]
