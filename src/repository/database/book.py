from datetime import datetime
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from core.models.book import Book
from core.models.order import BorrowRecord
from .base import BaseRepository
from repository import exception


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
            raise exception.BaseException

    async def get_books(self, offset: int, limit: int):
        try:
            books = (await self.session.execute(
                select(Book).offset(offset=offset).limit(limit=limit)
            )).scalars().all()
            return books
        except SQLAlchemyError as err:
            self.logger.error(f"Ошибки при получении книг: {err}")
            raise exception.BaseException

    async def update_book(self, data: dict, book_id: int) -> Book:
        try:
            async with self.session.begin():
                book = await self.session.get(Book, book_id)
                if not book:
                    raise exception.NotFoundException(msg=f"Book {book_id} not found")

                for key, value in data.items():
                    if hasattr(book, key):
                        setattr(book, key, value)

                await self.session.flush()
                self.logger.info(f"Book {book_id} updated")
                return book
                
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating book {book_id}: {e}")
            raise exception.BaseException

    async def get_book_with_borrow(self, book_id: int):
        result = (await self.session.execute(
            select(Book)
            .where(Book.id == book_id)
            .options(
                selectinload(Book.borrow_records).joinedload(BorrowRecord.reader)
            )
        )).scalars().first()
        if not result:
            raise exception.NotFoundException
        return result

    async def surch_book(
        self, 
        author: str | None = None, 
        title: str | None = None
    ):
        try:
            query = select(Book)
            
            if author:
                query = query.where(Book.author.like(f"%{author}%"))
            if title:
                query = query.where(Book.title.like(f"%{title}%"))
            
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as err:
            self.logger.error(f"Search book error: [{err}]")
            raise exception.BaseException
   