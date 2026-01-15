
#const { home } = require("../controllers/home_controller.js");
#router.get('/', home);

#module.exports = router;

from fastapi import APIRouter
from controllers.home_controller import home
from controllers.sample_controller import create_sample
#, delete_sample, find_sample,rql_sample
from models.sample import Sample


router = APIRouter(prefix="/api") #prefix="/users"

#Router-Controller Mapping

#sample
#add_or_update_sample
#add_environments
#add_publications
#add_measurements
#get_sample
#delete_sample
#router.get("/sample/find")(find_sample)
router.post("/sample/create",response_model=Sample,status_code=201,)(create_sample)
#router.delete("/sample/delete")(delete_sample)

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
