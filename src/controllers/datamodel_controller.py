from fastapi import Request, Body, Response, status
import urllib.parse
from typing import Dict, Any, Type
from fastapi.exceptions import RequestValidationError, HTTPException
from models.odm.datamodel import DataModel
from pydantic import ValidationError
from models.sample import Sample
from models.environment import Environment
from models.measurement import Reflectivity, EIS
from models.publication import Publication

datamodels={
    "sample":Sample,
    "environment":Environment,
    "reflectivity":Reflectivity,
    "eis":EIS,
    "publication":Publication
}


async def delete_dataobject(request:Request, datamodel: str,obj_id:str):
    session = request.state.dbsession
    cls_model = datamodels[datamodel]
    if cls_model is None:
        raise HTTPException(status_code=404, detail=f"Unknown datamodel '{datamodel}'")
    
    obj = cls_model.find_by_id(session, obj_id)
    if obj:
        obj.delete(session)
        return {"status":"success","deleted_id":obj_id}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_dataobject(request:Request, datamodel: str, obj_id:str):
    session = request.state.dbsession
    cls_model = datamodels[datamodel]
    if cls_model is None:
        raise HTTPException(status_code=404, detail=f"Unknown datamodel '{datamodel}'")
    
    #obj_id = urllib.parse.unquote(obj_id, encoding='utf-8', errors='strict')
    obj = cls_model.find_by_id(session, obj_id)
    return obj.view_object()


#Body(..., embed=True)
### valid JSON schema
##from the exact fields from the associated datamodel!
async def create_dataobject(request:Request,datamodel: str,data:dict = Body(...)):
    session = request.state.dbsession
    cls_model = datamodels[datamodel]
    if cls_model is None:
        raise HTTPException(status_code=404, detail=f"Unknown datamodel '{datamodel}'")
    #main fields
    errors=[]
    errors+=cls_model.validate_main_fields(data)
    
    #foreign keys validation
    for field in cls_model.get_foreign_key_fields():
        if field in data:
            errors+=cls_model.validate_foreign_keys(session,data[field],field)      
    if errors:
        raise RequestValidationError(errors)

    try:
        obj = cls_model.model_validate(data)
    except ValidationError as e:
        raise RequestValidationError(e.errors())

    doc = await obj.save(request.state.dbsession)
    return doc.view_object()

async def update_dataobject(request:Request,datamodel: str,obj_id:str, data:Dict[str,Any] = Body(..., embed=True)):
    session = request.state.dbsession
    cls_model = datamodels[datamodel]
    if cls_model is None:
        raise HTTPException(status_code=404, detail=f"Unknown datamodel '{datamodel}'")

    errors=[]
    session = request.state.dbsession
    data_obj = cls_model.find_by_id(session, obj_id)
    if (data_obj):
        
        #main fields
        errors+=cls_model.validate_main_fields(data)
        
        #foreign keys validation
        for field in cls_model.get_foreign_key_fields():
            if field in data:
                errors+=cls_model.validate_foreign_keys(session,data[field],field)      
        if errors:
            raise RequestValidationError(errors)
        
        #update field values
        for field, value in data.items():
           setattr(data_obj, field, value)
        
        doc = await data_obj.save(request.state.dbsession)
        return doc.view_object()
    
    #data_obj does not exist
    raise HTTPException(
            status_code=404,
            detail=f"{cls_model} with id '{obj_id}' not found"
        )
