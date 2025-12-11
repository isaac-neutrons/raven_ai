
#const { home } = require("../controllers/home_controller.js");
#router.get('/', home);

#module.exports = router;

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api") #prefix="/users"

@router.get("/")
async def list_users(request: Request):
    print("request.state: ", request.state.__dict__)
    session = request.state.dbsession
    #users = list(session.query(object_type=dict))
    users=["u1","u2"]
    return users