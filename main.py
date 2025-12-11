from fastapi import FastAPI
from fastmcp import FastMCP
from ravendb import DocumentStore
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

import uvicorn
import asyncio

from http_routes.routes import router as http_routers
from mcp_routes.routes import register_mcp_handlers

from settings import HTTP_PORT, HOST, RAVENDB_SERVER_URL, DB

#DB
store = DocumentStore(
    urls=RAVENDB_SERVER_URL,
    database=DB
)

store.initialize()
print("DB STATUS:", store._initialized)
if not store._initialized:
   print("DB Error: db cannot be initialized")
   exit(-1)

#middleware
class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        request.state.dbstore = store
        session = store.open_session()
        request.state.dbsession = session
        try:
            response = await call_next(request)
        finally:
            session.close() 
        return response

######  -------- HTTP ----------  ######   
#Create web server
app = FastAPI(title="HTTP App")
#middleware
app.add_middleware(DBSessionMiddleware)
# routers for http API endpoints
app.include_router(http_routers)

######  -------- MCP ----------  ######   
# Create an MCP server the FastAPI app
fastmcp = FastMCP.from_fastapi(app=app, name="MCP App")
asyncio.run(register_mcp_handlers(fastmcp))
mcp_app = fastmcp.http_app(path='/mcp')

print("mcp_app.routes", mcp_app.routes)


######  -------- SERVER RUN ----------  ######   

uvicorn.run(app=app, host=HOST, port=HTTP_PORT)



#example usage for mcp
# async def main():
#   result = await fastmcp.tool["mcp_echo"](message="hello world")
#   print(result) 
  
# asyncio.run(main())

