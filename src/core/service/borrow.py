from core.schemas.borrow import  (
    BorrowBookCreate, BorrowBookResponse, BorrowBookReturn,
    BorrowWithBookAndReader, BorrowFilter, ShortBorrowResponse
)
from core.models.order import BorrowRecord
from repository.database import borrow


class BorrowService:
    def __init__(self, session):
        self.repo = borrow.BorrowRepository(model=BorrowRecord, session=session)

    async def borrow_book(
        self, 
        borrow: BorrowBookCreate, 
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
        borrow: BorrowBookReturn
    ) -> BorrowBookResponse:
        borrow = await self.repo.return_book(
            reader_id=borrow.reader_id, 
            book_id=borrow.book_id
        )
        return BorrowBookResponse.model_validate(borrow)
    
    async def get_borrow_by_id(self, borrow_id: int) -> BorrowWithBookAndReader:
        borrow = await self.repo.get_borrow_with_book(borrow_id=borrow_id)
        return BorrowWithBookAndReader.model_validate(borrow)
    
    async def get_borrow_records(self, filter: BorrowFilter) -> list[BorrowBookResponse]:
        result = await self.repo.get_borrow_records(filter=filter.active)
        return [BorrowBookResponse.model_validate(borrow) for borrow in result]
    
    async def get_all_borrow(self, offset: int, limit: int):
        result = await self.repo.get_all_borrow_records(offset=offset, limit=limit)
        return [BorrowBookResponse.model_validate(borrow) for borrow in result]