from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repository.session import get_session
from core.service.librarian import LibrarianService
from core.service.book import BookService


def librarian_service(
    session: AsyncSession = Depends(get_session)
):
    return LibrarianService(session=session)

def book_service(
        session: AsyncSession = Depends(get_session)
):
    return BookService(session=session)

def currnet_user():
    pass