from fastapi import Request, Body
from models.sample import Sample,Layer
from models.material import Material
from models.environment import Environment



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

async def delete_sample(request:Request):
    session = request.state.dbsession
    sample = await Sample.find_by_id(session,"samples/610-A")
    if sample:
        sample.delete(session)
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
    