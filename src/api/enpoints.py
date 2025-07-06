from fastapi import APIRouter
from .routers import user

main_router = APIRouter()
main_router.include_router(user.router)