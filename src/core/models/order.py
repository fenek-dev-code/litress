from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from .base import Base  

if TYPE_CHECKING:
    from .book import Book
    from .reader import Reader
    from .librarian import Librarian

class BorrowRecord(Base):
    """
    Модель для учета выдачи книг читателям.
    Содержит информацию о каждой операции выдачи/возврата.
    """
    __tablename__ = "borrow_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(Integer, ForeignKey("readers.id"))
    librarian_id: Mapped[int] = mapped_column(Integer, ForeignKey("librarians.id"))

    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    return_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    book: Mapped["Book"] = relationship(back_populates="borrow_records")  
    reader: Mapped["Reader"] = relationship(back_populates="borrow_records")  
    librarian: Mapped["Librarian"] = relationship(back_populates="issued_books")

    def __repr__(self):
        return f"<BorrowRecord(book_id={self.book_id}, reader_id={self.reader_id}, returned={self.return_date is not None}>"