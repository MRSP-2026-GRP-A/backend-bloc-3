from fastapi import APIRouter
from app.services.hello_service import HelloService

router = APIRouter()

@router.get("/say-hello/{name}")
async def read_hello(name: str):
    message = HelloService.get_greeting(name)
    return {"message": message}