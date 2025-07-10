from core.models.reader import Reader
from core.models.order import BorrowRecord
from .base import BaseRepository
from core.exceptions import (
    ServerError, NotFoundError, ConflictBookError
)

from sqlalchemy import select, delete, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, joinedload

class ReaderRepository(BaseRepository[Reader]):

    async def get_readers(self, offset: int, limit: int):
        try:
            readers = await self.session.scalars(
                select(Reader).offset(offset=offset).limit(limit=limit)
            )
            return readers
        except SQLAlchemyError as e:
            self.logger.error(f"Get Readers Error[{e}]")
            pass


    async def create_with_librarian(self, email: str, name: str, librarian_id: int):
        try:
            existing = (await self.session.execute(
                select(Reader).where(Reader.email == email)
            )).scalar_one_or_none()

            if existing:
                raise ConflictBookError(message=f"Читатель с Email: {email} уже есть !")
            reader = Reader(email=email, name=name, librarian_id=librarian_id)
            self.session.add(reader)
            await self.session.commit()
            await self.session.refresh(reader)
            return reader
            
        except SQLAlchemyError as err:
            self.logger.error(f"Ошибки при создание читателя {email} : {err}")
            raise ServerError

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
            raise NotFoundError(message=f"Читатель {reader_id} не найден")
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
            raise NotFoundError(message=f"Читетль {reader_id} не найден")
          
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
            raise NotFoundError(message=f"Активных заказов нет")
            
        return borrow_records