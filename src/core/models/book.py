from sqlalchemy import Integer, String, CheckConstraint, func, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from .base import Base


class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)  # Добавлен лимит
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    pub_year: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[Optional[str]] = mapped_column(String(17), unique=True)  # ISBN-13 имеет 17 символов
    copies: Mapped[int] = mapped_column(Integer, nullable=False)
    librarian_id: Mapped[int] = mapped_column(Integer, ForeignKey("librarians.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    librarian: Mapped["Librarian"] = relationship(back_populates="books")

    __table_args__ = (
        Index('ix_book_author', 'author'),  
        Index('ix_book_title', 'title')   
    )