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


async def delete_dataobject(request:Request, datamodel: str,obj_id:str) -> dict:
    """
    It deletes a dataobject.

    :param datamodel: datamodel type from : [sample,environment,reflectivity,eis,publication].
    :type datamodel: str
    :param obj_id: object GUID Id
    :type obj_id: str
    :returns: the status completion and the deleted object id {"status":"success","deleted_id":obj_id}
    :rtype: dict    
    """

    session = request.state.dbsession
    cls_model = datamodels[datamodel]
    if cls_model is None:
        raise HTTPException(status_code=404, detail=f"Unknown datamodel '{datamodel}'")
    
    obj = cls_model.find_by_id(session, obj_id)
    if obj:
        obj.delete(session)
        return {"status":"success","deleted_id":obj_id}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_dataobject(request:Request, datamodel: str, obj_id:str) ->Sample | Environment | Reflectivity | EIS | Publication:
    """
    It finds and returns an active dataobject.

    :param datamodel: datamodel type from : [sample,environment,reflectivity,eis,publication].
    :type datamodel: str
    :param obj_id: object GUID Id
    :type obj_id: str
    :returns: the object with its fields
    :rtype: Sample | Environment | Reflectivity | EIS | Publication    
    """    
    session = request.state.dbsession
    cls_model = datamodels[datamodel]
    if cls_model is None:
        raise HTTPException(status_code=404, detail=f"Unknown datamodel '{datamodel}'")
    
    #obj_id = urllib.parse.unquote(obj_id, encoding='utf-8', errors='strict')
    obj = cls_model.find_by_id(session, obj_id)
    if obj:
        return obj.view_object()
    return None

#Body(..., embed=True)
### valid JSON schema
##from the exact fields from the associated datamodel!
async def create_dataobject(request:Request,datamodel: str,data:dict = Body(...)) ->Sample | Environment | Reflectivity | EIS | Publication:
    """
    It creates a new dataobject.

    :param datamodel: datamodel type from : [sample,environment,reflectivity,eis,publication].
    :type datamodel: str
    :param data: dict with all the fields and the values for an object 
    :type data: dict (POST body)
    :returns: the object with its fields
    :rtype: Sample | Environment | Reflectivity | EIS | Publication   
    """      
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
    if doc:
        return doc.view_object()
    return None

async def update_dataobject(request:Request,datamodel: str,obj_id:str, data:Dict[str,Any] = Body(..., embed=True)) ->Sample | Environment | Reflectivity | EIS | Publication:
    """
    It updates an active dataobject with  Id obj_id.

    :param datamodel: datamodel type from : [sample,environment,reflectivity,eis,publication].
    :type datamodel: str
    :param data: dict that contains the fields and the values that need to be updated to, replacing the exisiting values to the news ones
    :type data: dict
    :returns: the object with its fields
    :rtype: Sample | Environment | Reflectivity | EIS | Publication 
    """   

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
        if doc:
            return doc.view_object()
        return None
    
    #data_obj does not exist
    raise HTTPException(
            status_code=404,
            detail=f"{cls_model} with id '{obj_id}' not found"
        )
