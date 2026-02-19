from fastapi import APIRouter
from controllers.home_controller import home
# from controllers.sample_controller import create_sample, delete_sample, get_sample, update_sample
#rql_sample
# from models.sample import Sample
from controllers.datamodel_controller import create_dataobject,delete_dataobject,get_dataobject,update_dataobject
# from models.odm.datamodel import DataModel
router = APIRouter(prefix="/api") 

#Router-Controller Mapping

# #sample
# #get_sample
# router.get("/sample/get/{sample_id}")(get_sample)
# #add sample
# router.post("/sample/create",response_model=Sample,status_code=201,)(create_sample)
# #update sample
# router.post("/sample/update/{sample_id}",response_model=Sample,status_code=201,)(update_sample)

# #delete_sample
# router.delete("/sample/delete/{sample_id}")(delete_sample)




#get_sample
router.get("/{datamodel}/get/{obj_id}")(get_dataobject)
#add sample
router.post("/{datamodel}/create",status_code=201)(create_dataobject)
#delete_sample
router.delete("/{datamodel}/delete/{obj_id}")(delete_dataobject)
#update sample
router.post("/{datamodel}/update/{obj_id}",status_code=201,)(update_dataobject)


#last
router.get("/")(home)
