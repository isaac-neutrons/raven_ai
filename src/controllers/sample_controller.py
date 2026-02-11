from fastapi import Request, Body, Response, status
from models.sample import Sample,Layer
# from models.material import Material
# from models.environment import Environment
import urllib.parse
from typing import Dict, Any
from fastapi.exceptions import RequestValidationError, HTTPException


async def rql_sample(request:Request):
    session = request.state.dbsession
    query = "from Samples where id() = 'samples/641-A'"
    sample_list = Sample.raw_rql(session,query)
    return sample_list


async def find_sample(request:Request):
    state = request.state
    sample_list = list( \
        Sample.find_active(state) \
              .where_equals("description", "sample data") \
              .where_greater_than_or_equal("main_layer_index", 0)
        )
    return sample_list

async def delete_sample(request:Request, sample_id:str):
    session = request.state.dbsession
    sample = Sample.find_by_id(session, sample_id)
    if sample:
        sample.delete(session)
        return {"status":"success","deleted_id":sample_id}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_sample(request:Request, sample_id:str):
    session = request.state.dbsession
    obj_id = urllib.parse.unquote(sample_id, encoding='utf-8', errors='strict')
    sample = Sample.find_by_id(session, obj_id)
    print("sample",sample, obj_id, sample_id)
    return sample


#Body(..., embed=True)
### valid JSON schema

# {   
#     "description":"this is a test",
#     "environment_ids":["environments/100A"],
#     "substrate":
#     {
#         "material":{
#             "composition": "composition1",
#             "mass": 1.9,
#             "density":2.21
#         },
#         "thickness":1.2
#     },
#     "main_composition":"co3",
#     "geometry":"sq",
#     "layers":[
#         {
#             "material":{
#                 "composition": "composition1",
#                 "mass": 1.9,
#                 "density":2.21
#             },            
#             "thickness":1.3
#         },
#         {
#             "material":{
#                 "composition": "composition1",
#                 "mass": 1.9,
#                 "density":2.21
#             },
#             "thickness":1.2
#         }
#     ],
#     "publication_ids":[]
# }

async def create_sample(request:Request,sample:Sample = Body(...)):
    #print(request)
    print(sample)
    saved_sample = await sample.save(request.state.dbsession)
    return saved_sample
    
#here
async def update_sample(request:Request,sample_id:str, sample_data:Dict[str,Any] = Body(..., embed=True)):
    errors=[]
    session = request.state.dbsession
    sample = Sample.find_by_id(session, sample_id)
    if (sample):
        
        #main fields
        errors+=Sample.validate_main_fields(sample_data)
        
        #foreign keys validation
        for field in Sample.get_foreign_key_fields():
            if field in sample_data:
                errors+=Sample.validate_foreign_keys(session,sample_data[field],field)      
        if errors:
            raise RequestValidationError(errors)
        
        #update field values
        for field, value in sample_data.items():
           setattr(sample, field, value)
        
        saved_sample = await sample.save(request.state.dbsession)
        return saved_sample
    
    #sample does not exist
    raise HTTPException(
            status_code=404,
            detail=f"Sample with id '{sample_id}' not found"
        )
