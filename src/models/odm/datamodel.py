from pydantic import BaseModel, ValidationError, Field, ConfigDict
from typing import Optional, ClassVar, Type, List, Any, Dict
from ravendb import DocumentStore
import uuid

from datetime import datetime, timezone
from pydantic import ValidationError, TypeAdapter
from typing import Dict, Any,Annotated


class DataModel(BaseModel):
    """
    ODM model for RavenDB:
      - schema validation
      - CRUD operations, soft delete
      - collection auto-naming
      - simple queries
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
        if self.Id is None:
            # Generate GUID
            self.Id = str(uuid.uuid4())
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
    
    def view_object(self):
        #remove data management fields from the returned object
        data = self
        del data.is_deleted
        del data.created_at
        return data

    @classmethod
    def connect_to_store(cls, store: Any):
        cls._store = store

    #Find By Id    
    @classmethod
    def find_by_id(cls: Type["DataModel"],session, doc_id: str) -> Optional["DataModel"]:
        data=None
        data = session.load(doc_id, cls)
        print("data",data)
        try:
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

    #validation methods
    @classmethod
    def validate_main_fields(cls: Type["DataModel"], payload)-> List:
        errors = []
        model_fields = cls.model_fields

        for key, value in payload.items():
            #check if exists
            if key not in model_fields:
                errors.append({
                    "loc": ("body", "dict", key),
                    "msg": "extra field not permitted",
                    "type": "extra_forbidden",
                })
                continue
            #check if valid
            field = model_fields.get(key)
            #get field metadata if exist
            if field.metadata:
                annotated_type = Annotated[field.annotation, *field.metadata]
            else:
                annotated_type = field.annotation
            try:
                TypeAdapter(annotated_type).validate_python(value)
            except ValidationError as ve:
                for err in ve.errors():
                    errors.append({
                        "loc": ("body", "data") + tuple(err.get("loc", (key,))),
                        "msg": err.get("msg", "validation error"),
                        "type": err.get("type", "value_error"),
                    })
        return errors

    @classmethod
    def get_foreign_key_fields(cls):
        return []

    @classmethod
    def validate_foreign_keys(cls: Type["DataModel"],session, foreign_keys: list[str], field):
        errors=[]
        missing = []

        for i, obj_id in enumerate(foreign_keys):
            doc = session.load(obj_id)
            if doc is None:
                missing.append([i,obj_id])

        for [indx,obj_id] in missing:
            errors.append({
                "loc": ("body", "data", field, indx),
                "msg": f"Document with Id '{obj_id}' not found",
                "type": "value_error.foreign_key",
            })
        return errors