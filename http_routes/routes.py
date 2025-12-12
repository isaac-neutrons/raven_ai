
#const { home } = require("../controllers/home_controller.js");
#router.get('/', home);

#module.exports = router;

from fastapi import APIRouter
from controllers.home_controller import home, list_users, create_sample, delete_sample



router = APIRouter(prefix="/api") #prefix="/users"

#Router-Controller Mapping
router.get("/users")(list_users)
router.get("/sample/create")(create_sample)
router.get("/sample/delete")(delete_sample)


#last
router.get("/")(home)
