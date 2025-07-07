from fastapi import APIRouter
from .routers import user, book

main_router = APIRouter()
main_router.include_router(user.router)
main_router.include_router(book.router)