
from sqlalchemy.ext.asyncio import AsyncSession
from repository.database.book import BookRepository
from core.models.book import Book

class BookService:
    def __init__(self, session: AsyncSession):
        self.repo = BookRepository(model=Book, session=session)

    