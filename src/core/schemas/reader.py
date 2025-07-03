from pydantic import BaseModel, EmailStr, Field, conlist
from typing import List, Optional
from datetime import datetime

from .book import ResponseBook

class BaseReader(BaseModel):
    """
    Базовая модель читателя с валидацией полей
    
    Attributes:
        name: Полное имя читателя (2-100 символов)
        email: Валидный email-адрес
    """
    name: str = Field(..., min_length=2, max_length=100, example="Иван Иванов")
    email: EmailStr = Field(..., example="reader@example.com")

class CreateReader(BaseReader):
    """
    Модель для создания нового читателя
    
    Example:
        ```json
        {
            "name": "Анна Петрова",
            "email": "anna@example.com"
        }
        ```
    """
    pass

class ResponseReader(BaseReader):
    """
    Модель ответа с данными читателя
    
    Attributes:
        reader_id: Уникальный ID в системе
        librarian_id: ID ответственного библиотекаря
        created_at: Дата регистрации
        books: Список взятых книг (может быть пустым)
    """
    reader_id: int = Field(..., example=42)
    librarian_id: Optional[int] = Field(None, example=1)  
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z")
    books: List["ResponseBook"] = []

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() 
        }


class UpdateReader(BaseModel):
    """
    ```json
    {
        "name": "Новое Имя Читателя",
        "email": "new.email@example.com"
    }
    ```
    Или для изменения только имени:
    ```json
    {
        "name": "Только новое имя"
    }
    ```
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


class ShortReaderResponse(BaseModel):
    """
    Attributes:
        reader_id: Уникальный идентификатор читателя в системе (primary key)
        name: Полное имя читателя в формате "Фамилия Имя"
    ```json
    {
        "reader_id": 42,
        "name": "Иванов Иван"
    }
    ```
    """
    reader_id: int
    name: str