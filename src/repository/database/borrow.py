from .base import BaseRepository
from core.models.order import BorrowRecord
from core.models.book import Book
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from core.exceptions import (
    NotFoundError, ServerError, BookLimitError
)

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
                    raise NotFoundError(message=f"Книга {book_id} не найдена!")
                if book.copies < 1:
                    raise NotFoundError(message=f"Книги {book_id} нет в наличии")
                
                active_borrows = await self.session.scalar(
                    select(func.count(BorrowRecord.id)).where(
                        BorrowRecord.reader_id == reader_id, 
                        BorrowRecord.return_date.is_(None)
                    )
                )

                if active_borrows >= 3:
                    raise BookLimitError(message=f"У вас слишком много книг, в аренду можно брать не более 3х")
                
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
        # except (BorrowLimit, NotFoundBook):
        #     raise

        except SQLAlchemyError as e:
            self.logger.error(f"DB Ошибка при выдаче книги ! \nBook_id: {book_id} \nReder_id:{reader_id} \nLibrarian_id: {librarian_id} {str(e)}")
            raise ServerError


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
                    raise NotFoundError(message=f"Заказ не найден")
                order = (await self.session.execute( 
                    select(BorrowRecord).where(
                        BorrowRecord.book_id == book_id,
                        BorrowRecord.reader_id == reader_id,
                        BorrowRecord.return_date.is_(None)  
                ))).scalar_one_or_none()
                if not order:
                    raise NotFoundError(message=f"Заказ не найден")
                order.return_date = datetime.now()
                book.copies += 1
                
                self.logger.info(f"Книга {book_id} успешно возвращена читателем {reader_id}")
        except SQLAlchemyError as e:
            self.logger.error(f"При возрате книги {book_id} читателем {reader_id} произошла ошибка: {e}")
            raise ServerError
        
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
                )).scalar()
                if not borrow:
                    raise NotFoundError(message=f"Заказ {borrow_id} не найден")
                return borrow
            
        except SQLAlchemyError as e:
            self.logger.error(f"Database error fetching borrow record {borrow_id}: {str(e)}")
            raise ServerError
        
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
            raise ServerError
        
    async def get_all_borrow_records(self, offset: int, limit: int):
        try:
            result = await self.session.scalars((
                select(BorrowRecord))
                .offset(offset)
                .limit(limit)
            )
            return result.all()
        except SQLAlchemyError as err:
            self.logger.error(f"Error where get all borrow Error: {err}")
            raise ServerError
