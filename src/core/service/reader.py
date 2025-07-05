from repository.database.reader import ReaderRepository
from core.models.reader import Reader
from core.schemas.reader import ShortReaderResponse, CreateReader, ResponseReade, ReaderWithBooksResponse

class ReaderService:
    def __init__(self, session):
        self.repo = ReaderRepository(model=Reader, session=session)
    
    async def create_reader(
        self, 
        new_reader: CreateReader, 
        librarian_id: int
    ) -> ShortReaderResponse:
        db_reader = await self.repo.create_with_librarian(**new_reader.model_dump(), librarian_id=librarian_id)
        return ShortReaderResponse.model_validate(db_reader)
    
    async def get_with_borrow_books(self, reader_id: int):
        reader = await self.repo.get_with_borrowed_books(reader_id=reader_id)
        return ReaderWithBooksResponse.model_validate(reader)