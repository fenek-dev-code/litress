from core.schemas.borrow import  BorrowBookResponse, BorrowBooksBase
from core.models.book import Book
from repository.database import book


class BorrowService:
    def __init__(self, session):
        self.repo = book.BookRepository(model=Book, session=session)

    async def borrow_book(
        self, 
        borrow: BorrowBooksBase, 
        librarian_id: int
    ) -> BorrowBookResponse:
        borrow_book = await self.repo.borrow_book(
            book_id=borrow.book_id, 
            reader_id=borrow.reader_id, 
            librarian_id=librarian_id
        )
        return BorrowBookResponse.model_validate(borrow_book)
    
    async def return_book(
        self, 
        borrow: BorrowBooksBase
    ) -> BorrowBookResponse:
        borrow = await self.repo.return_book(
            reader_id=borrow.reader_id, 
            book_id=borrow.book_id
        )
        return BorrowBookResponse.model_validate(borrow)