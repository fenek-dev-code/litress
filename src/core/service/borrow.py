from core.schemas.orders import BorrowRecordBase, BorrowRecordCreate, BorrowRecordResponse, BorrowRecordReturn
from repository.database import book
import logging

class BorrowService:
    def __init__(
        self,
        repository: book.BookRepository
    ):
        self.repo = repository
        self.logger = logging.getLogger(__name__)

    async def borrow_book(
        self, 
        borrow: BorrowRecordBase, 
        librarian_id: int
    ) -> BorrowRecordResponse:
        return await self.repo.borrow_book(
            book_id=borrow.book_id, 
            reader_id=borrow.reader_id, 
            librarian_id=librarian_id
        )

    
    async def return_book(
        self, 
        borrow: BorrowRecordBase
    ) -> BorrowRecordResponse:
        return await self.repo.return_book(
            reader_id=borrow.reader_id, 
            book_id=borrow.book_id
        )