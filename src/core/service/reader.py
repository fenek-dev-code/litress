from repository.database.reader import ReaderRepository
from core.models.reader import Reader
from core.schemas.reader import ShortReaderResponse, CreateReader, ResponseReader, ReaderWithRecordsResponse, ResponseReaderWithBooks

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
    
    async def get_readers(self, offset: int, limit: int) -> list[ResponseReader]:
        readers_db = await self.repo.get_readers(offset, limit)
        return [ResponseReader.model_validate(r) for r in readers_db]
    
    async def get_with_borro(self, reader_id: int) -> ReaderWithRecordsResponse:
        reader_db = await self.repo.get_active_borrow()
        return ReaderWithRecordsResponse.model_validate(reader_db)

    async def get_with_borrow_books(self, reader_id: int) -> ResponseReaderWithBooks:
        reader_db = await self.repo.get_with_borrowed_books(reader_id=reader_id)
        return ResponseReaderWithBooks.model_validate(reader_db)
    