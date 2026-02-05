
#const { home } = require("../controllers/home_controller.js");
#router.get('/', home);

#module.exports = router;

from fastapi import APIRouter
from controllers.home_controller import home
from controllers.sample_controller import create_sample, delete_sample, get_sample, update_sample
#rql_sample
from models.sample import Sample


router = APIRouter(prefix="/api") #prefix="/users"

#Router-Controller Mapping

#sample
#get_sample
router.get("/sample/get/{sample_id}")(get_sample)
#add sample
router.post("/sample/create",response_model=Sample,status_code=201,)(create_sample)
#update sample
#router.post("/sample/update/{sample_id}",response_model=Sample,status_code=201,)(update_sample)

#delete_sample
router.delete("/sample/delete/{sample_id}")(delete_sample)


#add_environments
#add_publications
#add_measurements


#reflectivity
#add_or_update_reflectivity
#get_reflectivities
#delete_reflectivity

#eis
#add_or_update_eis
#get_eis
#delete_eis

#environment
#add_or_update_environment
#get_environments
#delete_environment

#publication
#add_or_update_publication
#get_publications
#delete_publication

#router.get("/users")(list_users)

#router.get("/sample/rql")(rql_sample)


#last
router.get("/")(home)
