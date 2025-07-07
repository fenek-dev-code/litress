from typing import List  
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base
from .book import Book
from .librarian import Librarian

class Reader(Base):
    """
    Модель читателя/пользователя библиотеки.
    Содержит информацию о читателе и его связях с книгами и библиотекарями.
    """
    __tablename__ = "readers" 

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    """
    Уникальный идентификатор читателя в системе.
    Автоматически генерируется при создании записи.
    """

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """
    Полное имя читателя. Ограничение:
    - Максимальная длина: 100 символов
    - Обязательное поле (не может быть NULL)
    """

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    """
    Электронная почта читателя. Ограничения:
    - Максимальная длина: 255 символов
    - Должен быть уникальным в системе
    - Обязательное поле
    """

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    """
    Дата и время регистрации читателя. Автоматически устанавливается 
    в текущую дату/время при создании записи.
    """

    # Связи с другими таблицами
    librarian_id: Mapped[int] = mapped_column(Integer, ForeignKey("librarians.id"))
    """
    Внешний ключ к таблице библиотекарей (librarians).
    Указывает, какой библиотекарь зарегистрировал читателя.
    """

    librarian: Mapped["Librarian"] = relationship(back_populates="readers") # type: ignore
    """
    Отношение "многие-к-одному" с моделью Librarian.
    Обеспечивает доступ к данным связанного библиотекаря.
    """

    borrow_records: Mapped[List["BorrowRecord"]] = relationship(
        back_populates="reader"
    )
    """
    Отношение "один-ко-многим" с моделью Book.
    Список книг, связанных с данным читателем.
    """