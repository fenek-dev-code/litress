from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import datetime
from typing import Optional, List

from .borrow import ShortBorrowResponse

class BaseBook(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=200,
        example="Преступление и наказание",
        description="Название книги"
    )
    author: str = Field(
        ...,
        min_length=2,
        max_length=100,
        example="Фёдор Достоевский",
        description="Автор книги"
    )
    pub_year: Optional[int] = Field(
        None,
        ge=1800,
        le=datetime.now().year,
        example=1866,
        description="Год публикации (от 1800 до текущего года)"
    )
    copies: int = Field(
        ge=1,
        le=1000,
        default=1,
        example=5,
        description="Количество доступных копий"
    )
    model_config = ConfigDict(from_attributes=True)

class CreateBook(BaseBook):
    """"""

class ResponseBook(BaseBook):
    book_id: int = Field(..., example=42, description="Уникальный ID книги", validation_alias="id")
    librarian_id: int = Field(..., example=1, description="ID библиотекаря, добавившего книгу")
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z", description="Дата добавления в каталог")




class ShortBookResponse(BaseModel):
    book_id: int = Field(..., example=1, description="Уникальный ID книги", validation_alias="id")
    title: str = Field(..., example="1984", description="Название книги")
    author: str = Field(..., example="Джордж Оруэлл", description="Автор книги")
    pub_year: Optional[int] = Field(None, example=1949, description="Год публикации")
    class Config:
        from_attributes = True

class UpdateBook(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=2,
        max_length=200,
        example="Новое название",
        description="Обновленное название книги"
    )
    author: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        example="Новый автор",
        description="Обновленный автор книги"
    )
    pub_year: Optional[int] = Field(
        None,
        ge=1800,
        le=datetime.now().year,
        example=2020,
        description="Обновленный год публикации"
    )
    copies: Optional[int] = Field(
        None,
        ge=1,
        le=1000,
        example=10,
        description="Обновленное количество копий"
    )
    


class ResponseBookWithBorrow(ShortBookResponse):
    borrow_records: List["ShortBorrowResponse"] = Field(  
        default_factory=list,
        example=[{
            "record_id": 1,
            "borrow_date": "2023-05-01T14:30:00Z",
            "return_date": None
        }],
        description="История выдачи данной книги"
    )



class BookSearchFilters(BaseModel):
    title: Optional[str] = Field(
        None,
        example="Война",
        description="Часть названия для поиска (регистронезависимо)"
    )
    author: Optional[str] = Field(
        None,
        example="Толстой",
        description="Часть имени автора для поиска (регистронезависимо)"
    )
    year_from: Optional[int] = Field(
        None,
        ge=1800,
        le=datetime.now().year,
        example=1900,
        description="Минимальный год публикации"
    )
    year_to: Optional[int] = Field(
        None,
        le=datetime.now().year,
        example=2000,
        description="Максимальный год публикации"
    )
    
