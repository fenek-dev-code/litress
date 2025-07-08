from .base import BaseRepository
from repository import exception
from core.models.order import BorrowRecord
from core.models.book import Book
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from datetime import datetime


class BorrowRepository(BaseRepository[BorrowRecord]):

    async def borrow_book(
        self, 
        book_id: int, 
        reader_id: int, 
        librarian_id: int
    ) -> BorrowRecord:
        self.logger.info(f"Попытка выдачи книги {book_id} читателю {reader_id}")
        try:
            async with self.session.begin():
                book = await self.session.get(Book, book_id)
                if not book:
                    raise exception.NotFoundException("Книга не найдена")
                if book.copies < 1:
                    raise exception.NotFoundException("Нет доступных экземпляров этой книги")
                
                active_borrows = await self.session.scalar(
                    select(func.count(BorrowRecord.id)).where(
                        BorrowRecord.reader_id == reader_id, 
                        BorrowRecord.return_date.is_(None)
                    )
                )

                if active_borrows >= 3:
                    raise exception.LimmitException
                
                record = BorrowRecord(
                    book_id=book_id,
                    reader_id=reader_id,
                    librarian_id=librarian_id,
                    borrow_date=datetime.now()
                )
                
                book.copies -= 1
                record.book = book
                self.session.add(record)
                await self.session.flush()
                return record
        except (exception.NotFoundException, exception.LimmitException):
            raise

        except SQLAlchemyError as e:
            self.logger.error(f"DB Ошибка при выдаче книги ! \nBook_id: {book_id} \nReder_id:{reader_id} \nLibrarian_id: {librarian_id} {str(e)}")
            raise exception.BaseException


    async def return_book(
        self, 
        reader_id: int, 
        book_id: int
    ):
        self.logger.info(f"Попоытка вернуть книгу: RedaerID: {reader_id}, BookID: {book_id}")
        try:
            async with self.session.begin():
                book = await self.session.get(Book, book_id)
                if not book:
                    raise exception.NotFoundException()
                order = (await self.session.execute( 
                    select(BorrowRecord).where(
                        BorrowRecord.book_id == book_id,
                        BorrowRecord.reader_id == reader_id,
                        BorrowRecord.return_date.is_(None)  
                ))).scalar_one_or_none()
                if not order:
                    raise exception.NotFoundException
                order.return_date = datetime.now()
                book.copies += 1
                
                self.logger.info(f"Книга {book_id} успешно возвращена читателем {reader_id}")
        except SQLAlchemyError as e:
            self.logger.error(f"При возрате книги {book_id} читателем {reader_id} произошла ошибка: {e}")
            raise exception.BaseException
        
    async def get_borrow_with_book(self, borrow_id: int):
        try:
            async with self.session.begin():
                borrow = (await self.session.execute(
                    select(BorrowRecord).where(
                        BorrowRecord.id == borrow_id
                    ).options(
                        selectinload(BorrowRecord.book),
                        selectinload(BorrowRecord.reader)
                    )
                )).scalar_one()
                if not borrow:
                    raise exception.NotFoundException(f"Borrow record {borrow_id} not found")
                return borrow
            
        except NoResultFound as e:
            self.logger.error(f"Borrow record not found: ID {borrow_id}")
            raise exception.NotFoundException(f"Borrow record {borrow_id} not found") from e
        
        except SQLAlchemyError as e:
            self.logger.error(f"Database error fetching borrow record {borrow_id}: {str(e)}")
            raise exception.BaseException(f"Error accessing borrow record {borrow_id}") from e
        
    async def get_borrow_records(self, filter: bool = True):
        try:
            if filter == True:
                result = (await self.session.execute(
                    select(BorrowRecord).where(
                        BorrowRecord.return_date.is_not(None) 
                    )
                ))
                return result.scalars().all()
            result = (await self.session.execute(
                select(BorrowRecord).where(
                    BorrowRecord.return_date.is_(None)
                )
            ))
            return result.scalars().all()
        except SQLAlchemyError as err:
            self.logger.error(f"Get Borrow records Error [{err}]")
            raise exception.BaseException
        
    async def get_all_borrow_records(self, offset: int, limit: int):
        try:
            pass
        except SQLAlchemyError as err:
            pass
