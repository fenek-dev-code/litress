from core.models.reader import Reader
from core.models.order import BorrowRecord
from .base import BaseRepository
from repository.exception import ReaderConflict, ReaderException, ReaderNotFound

from sqlalchemy import select, delete, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

class ReaderRepository(BaseRepository):

    async def create_with_librarian(self, email: str, name: str, librarian_id: int):
        try:
            existing = (await self.session.execute(
                select(Reader).where(Reader.email == email)
            )).scalar_one_or_none()

            if existing:
                raise ReaderConflict

            async with self.session.begin():
                reader = Reader(email=email, name=name, librarian_id=librarian_id)
                await self.session.add(reader)
                await self.session.flush()
                return reader
            
        except SQLAlchemyError as err:
            self.logger.error(f"Ошибки при создание читателя {reader.email} : {err}")
            raise ReaderException

    async def get_with_borrowed_books(self, reader_id: int):
        result = (await self.session.execute(
            select(Reader)
            .where(Reader.id == reader_id)
            .options(
                selectinload(Reader.borrow_records)
                .joinedload(BorrowRecord.book)
            )
        )).scalar_one_or_none()
        
        if not result:
            raise ReaderNotFound
        
        return result

    
    async def count_active_borrows(self, reader_id: int):
        result = (await self.session.scalar(
            select(func.count())
            .where(
                BorrowRecord.reader_id == reader_id,
                BorrowRecord.return_date.is_(None)
            )
        )) 
        return result or 0
            
    
    async def delete_reader(self, reader_id: int): 
        try:
            async with self.session.begin():
                result = await self.session.execute(
                    delete(Reader).filter(Reader.id == reader_id)
                )
                if result.rowcount == 0:
                    raise ReaderNotFound
                self.logger.info(f"Читатель {reader_id} был удалён")
        except SQLAlchemyError as err:
            self.logger.error(f"При удаление читателя {reader_id} возникла ошибка: {err}")
            raise ReaderException
