from fastapi import Request


async def home(request:Request):
    return {"message": "Welcome to Home"}
