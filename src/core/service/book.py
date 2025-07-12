
from sqlalchemy.ext.asyncio import AsyncSession
from repository.database.book import BookRepository
from core.models.book import Book
from core.schemas.book import CreateBook, ResponseBook, UpdateBook, ResponseBookWithBorrow, ShortBookResponse, BookSearchFilters
from core.exceptions import NotFoundError


class BookService:
    def __init__(self, session: AsyncSession):
        self.repo = BookRepository(model=Book, session=session)

    async def create_book(self, new_book: CreateBook, librarian_id: int) -> ResponseBook:
        book_data = new_book.model_dump()
        book_model = Book(**book_data, librarian_id=librarian_id)
        book = await self.repo.create_book(book_model)
        return ResponseBook.model_validate(book)
    
    async def get_book(self, id: int) -> ShortBookResponse:
        db_book = await self.repo.get(id)
        if not db_book:
            raise NotFoundError(message=f"Книга {id} не найдена")
        return ShortBookResponse.model_validate(db_book)

    async def update_book(self, book_id: int, book: UpdateBook) -> ResponseBook:
        book_data = book.model_dump() 
        new_book = await self.repo.update_book(book_data, book_id=book_id)
        return ResponseBook.model_validate(new_book)

    async def delete_book(self, book_id: int):
        result = await self.repo.delete(book_id) 
        print(result)
        if result:
            return True
        raise NotFoundError(f"Книга {book_id} не найдена")

    async def get_book_with_borrow(self, book_id: int) -> ResponseBookWithBorrow:
        book = await self.repo.get_book_with_borrow(book_id)
        return ResponseBookWithBorrow.model_validate(book)
    
    async def get_books(self, offset: int, limit: int) -> list[ShortBookResponse]:
        db_books = await self.repo.get_books(offset=offset, limit=limit)
        return [ShortBookResponse.model_validate(b) for b in db_books]
    
    async def search_book(
            self, 
            search_data: BookSearchFilters
    ) -> list[ShortBookResponse]:
        db_books = await self.repo.surch_book(
            author=search_data.author, 
            title=search_data.title,
        )
        return [ShortBookResponse.model_validate(b) for b in db_books]
    