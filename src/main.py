from fastapi import FastAPI
from fastmcp import FastMCP
from ravendb import DocumentStore
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import uvicorn
import asyncio

from http_routes.routes import router as http_routers
from mcp_routes.routes import register_mcp_handlers
from models.odm.datamodel import DataModel
from settings import HTTP_PORT, HOST, RAVENDB_SERVER_URL, DB


if __name__ == '__main__':

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

    #pass DB store to DataModel
    DataModel.connect_to_store(store)

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
    
    #validation exception halder response format close to RFC 7807
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Convert FastAPI/Pydantic errors into RFC7807-like shape
        invalid_params = []
        for e in exc.errors():
            field_path = [str(x) for x in e.get("loc", [])] 
            message = e.get("msg", "Invalid value")
            type_error = e.get("type", "validation_error")
            invalid_params.append({
                "name": ".".join(field_path),
                "reason": message,
                "type": type_error,
            })

        problem = {
            "type": "https://raven-ai.readthedocs.io/", # point to documentation for error
            "title": "Request validation failed",
            "status": 422,
            "detail": "One or more fields have invalid values.",
            "instance": str(request.url.path),
            "invalid_params": invalid_params,
        }

        return JSONResponse(
            status_code=422,
            content=problem,
            media_type="application/problem+json",
        )

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

