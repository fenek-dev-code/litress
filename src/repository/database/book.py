from datetime import datetime
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from core.models.book import Book
from core.models.order import BorrowRecord
from .base import BaseRepository
from repository.exception import BookNotFound, NotFoundException, DataBaseErrorExceprion, ConflictException, DataBaseErrorExceprion


class BookRepository(BaseRepository[Book]):

    async def create_book(self, new_book: Book):
        try: 
            async with self.session.begin():
                self.session.add(new_book)
                await self.session.flush()
                self.logger.info(f"Книга {new_book.id} была созданна")
                return new_book
        except SQLAlchemyError as e:
            self.logger.error(f"Ошибка при создание книги: {e}")
            raise DataBaseErrorExceprion("Failed to create book")

    async def get_book_by_id(self, book_id: int) -> Book:
        try:
            book = await self.session.get(Book, book_id)
            if not book:
                raise NotFoundException(f"Book {book_id} not found")
            return book
        except SQLAlchemyError as e:
            self.logger.error(f"DB error fetching book {book_id}: {e}")
            raise DataBaseErrorExceprion("Database operation failed")

    async def update_book(self, data: dict, book_id: int) -> Book:
        try:
            async with self.session.begin():
                book = await self.session.get(Book, book_id)
                if not book:
                    raise NotFoundException(f"Book {book_id} not found")

                for key, value in data.items():
                    if hasattr(book, key):
                        setattr(book, key, value)

                await self.session.flush()
                self.logger.info(f"Book {book_id} updated")
                return book
                
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating book {book_id}: {e}")
            raise DataBaseErrorExceprion("Update operation failed")

    async def delete_book(self, book_id: int) -> None:
        try:
            async with self.session.begin():
                result = await self.session.execute(
                    delete(Book).where(Book.id == book_id)
                )
                if result.rowcount == 0:
                    raise NotFoundException(f"Book {book_id} not found")
                self.logger.info(f"Book {book_id} deleted")
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting book {book_id}: {e}")
            raise DataBaseErrorExceprion("Delete operation failed")

    async def get_book_with_borrow(self, book_id: int):
        result = (await self.session.execute(
            select(Book)
            .where(Book.id == book_id)
            .options(
                selectinload(Book.borrow_records).joinedload(BorrowRecord.reader)
            )
        )).scalars().first()
        if not result:
            raise BookNotFound
        return result

    async def surch_book(
        self, 
        author: str | None = None, 
        title: str | None = None
    ):
        query = select(Book)
        
        if author:
            query = query.where(Book.author.like(f"%{author}%"))
        if title:
            query = query.where(Book.title.like(f"%{title}%"))
        
        result = await self.session.execute(query)
        return result.scalars().all()

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
                    raise NotFoundException("Книга не найдена")
                if book.copies < 1:
                    raise NotFoundException("Нет доступных экземпляров этой книги")
                
                active_borrows = (await self.session.execute(
                    select(func.count()).where(
                    BorrowRecord.reader_id == reader_id,
                    BorrowRecord.return_date.is_(None)
                ))).scalar()

                if active_borrows >= 3:
                    raise ConflictException("Читатель уже имеет максимальное количество книг (3)")
                
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
                self.logger.info()
                return record
        except NoResultFound as e:
            self.logger.error(f"Ошибка при выдаче книги {book_id} читателю {reader_id}")
            raise DataBaseErrorExceprion("")

        except SQLAlchemyError as e:
            self.logger.error(f"DB Ошибка при выдаче книги ! \nBook_id: {book_id} \nReder_id:{reader_id} \nLibrarian_id: {librarian_id} {str(e)}")
            raise

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
                    raise NotFoundException()
                order = (await self.session.execute( 
                    select(BorrowRecord).where(
                        BorrowRecord.book_id == book_id,
                        BorrowRecord.reader_id == reader_id,
                        BorrowRecord.return_date.is_(None)  
                ))).scalar_one_or_none()
                if not order:
                    raise 
                order.return_date = datetime.now()
                book.copies += 1
                
                self.logger.info(f"Книга {book_id} успешно возвращена читателем {reader_id}")
        except SQLAlchemyError as e:
            self.logger.error(f"При возрате книги {book_id} читателем {reader_id} произошла ошибка: {e}")
            raise DataBaseErrorExceprion()