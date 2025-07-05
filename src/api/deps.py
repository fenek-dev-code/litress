from fastapi import Depends
from repository.session import get_session
from core.models.librarian import Librarian
from core.models.book import Book
from repository.database.librarian import LibrarianRepository
from repository.database.book import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession

def get_librarian_db(
    session: AsyncSession = Depends(get_session)
):
    return LibrarianRepository(model=Librarian, sessio=session) 

def get_book_db(
        session: AsyncSession = Depends(get_session)
):
    return BookRepository(model=Book, session=session)

def get_current_user():
    pass