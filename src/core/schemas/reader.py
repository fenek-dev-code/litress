from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

from .book import ShortBookResponse
from .borrow import ShortBorrowResponse

class BaseReader(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        example="Иван Иванов",
        description="Полное имя читателя"
    )
    email: EmailStr = Field(
        ...,
        example="reader@example.com",
        description="Контактный email читателя"
    )
    model_config = ConfigDict(from_attributes=True)

class CreateReader(BaseReader):
    """"""

class ResponseReader(BaseReader):
    reader_id: int = Field(..., example=42, description="Уникальный ID читателя", validation_alias="id")
    librarian_id: Optional[int] = Field(
        None,
        example=1,
        description="ID библиотекаря, зарегистрировавшего читателя"
    )
    created_at: datetime = Field(
        ...,
        example="2023-01-15T10:30:00Z",
        description="Дата и время регистрации"
    )
    

class UpdateReader(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        example="Иван Петров",
        description="Новое имя читателя"
    )
    email: Optional[EmailStr] = Field(
        None,
        example="new.email@example.com",
        description="Новый email читателя"
    )
    


class ShortReaderResponse(BaseModel):
    reader_id: int = Field(..., example=42, description="Уникальный ID читателя", validation_alias="id")
    name: str = Field(..., example="Иван Иванов", description="Полное имя читателя")
    model_config = ConfigDict(from_attributes=True)


class ResponseReaderWithBooks(ShortReaderResponse):
    books: List["ShortBookResponse"] = Field(  
        default_factory=list,
        example=[{
            "book_id": 1,
            "title": "Война и мир",
            "author": "Лев Толстой"
        }],
        description="Список книг, взятых читателем"
    )

class ReaderWithRecordsResponse(ShortReaderResponse):
    email: str = Field(..., example="reader@example.com", description="Email читателя")
    borrow_records: List["ShortBorrowResponse"] = Field( 
        default_factory=list,
        example=[{
            "record_id": 1,
            "borrow_date": "2023-01-10T14:30:00Z",
            "return_date": None
        }],
        description="История выдачи книг читателю"
    )
