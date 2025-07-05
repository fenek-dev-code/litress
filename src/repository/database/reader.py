from core.models.reader import Reader
from core.models.order import BorrowRecord
from .base import BaseRepository
from repository import exception

from sqlalchemy import select, delete, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, joinedload

class ReaderRepository(BaseRepository[Reader]):

    async def create_with_librarian(self, email: str, name: str, librarian_id: int):
        try:
            existing = (await self.session.execute(
                select(Reader).where(Reader.email == email)
            )).scalar_one_or_none()

            if existing:
                raise exception.ConflictException

            async with self.session.begin():
                reader = Reader(email=email, name=name, librarian_id=librarian_id)
                await self.session.add(reader)
                await self.session.flush()
                return reader
            
        except SQLAlchemyError as err:
            self.logger.error(f"Ошибки при создание читателя {reader.email} : {err}")
            raise exception.BaseException

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
            raise exception.NotFoundException
        return result

    
    async def count_active_borrows(self, reader_id: int):
        result = await self.session.scalar(
            select(func.count())
            .where(
                BorrowRecord.reader_id == reader_id,
                BorrowRecord.return_date.is_(None)
            )
        )
        return result or 0
            

    async def get_active_borrow(self, reader_id: int):
        reader = await self.session.get(Reader, reader_id)
        if not reader:
            raise exception.NotFoundException("Reader not found")
          
        result = await self.session.execute(
            select(BorrowRecord)
            .where(
                BorrowRecord.reader_id == reader_id,
                BorrowRecord.return_date.is_(None)
            )
            .options(joinedload(BorrowRecord.book)) 
        )
        borrow_records = result.scalars().all()

        if not borrow_records:
            raise exception.NotFoundException("No active borrows found")
            
        return borrow_records