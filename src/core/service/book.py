
from sqlalchemy.ext.asyncio import AsyncSession
from repository.database.book import BookRepository
from core.models.book import Book
from core.schemas.book import CreateBook, ResponseBook, UpdateBook



class BookService:
    def __init__(self, session: AsyncSession):
        self.repo = BookRepository(model=Book, session=session)

    async def create_book(self, new_book: CreateBook, librarian_id: int) -> ResponseBook:
        book = Book(**CreateBook.dict()).librarian_id = librarian_id
        return await self.repo.create_book(book)
    
    async def get_book(self, id: int) -> ResponseBook:
        return await self.repo.get(id)

    async def delete_book(self, id: int):
        return await self.repo.delete(id) 

    async def get_book_with_borrow(self, book_id: int) -> ResponseBook:
        return await self.repo.get_book_with_borrow(book_id)
    
    async def get_books(self, offset: int, limit: int) -> list[ResponseBook]:
        return await self.repo.get_books(offset=offset, limit=limit)
    
    async def search_book(
            self, 
            autor: str | None = None, 
            title: str | None = None
    ) -> list[ResponseBook]:
        return await self.repo.surch_book(author=autor, title=title)
    
    