from fastapi import APIRouter
from .routers import user, book, reader, borrow

main_router = APIRouter()
main_router.include_router(user.router)
main_router.include_router(book.router)
main_router.include_router(reader.router)
main_router.include_router(borrow.router)