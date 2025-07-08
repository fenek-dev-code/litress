from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .book import ResponseBook
    from .reader import ResponseReader



class BorrowBooksBase(BaseModel):
    book_id: int = Field(..., example=1, description="ID книги")
    reader_id: int = Field(..., example=1, description="ID читателя")
    class Config:
        from_attributes = True


class BorrowBookCreate(BorrowBooksBase):
    librarian_id: int = Field(..., example=1, description="ID библиотекаря")  # Исправлено: examples -> example


class BorrowBookReturn(BorrowBooksBase):
    """ Return Book Shema"""

class BorrowFilter(BaseModel):
    active: bool | None = None

class BorrowBookResponse(BorrowBooksBase):
    record_id: int = Field(..., description="ID записи о выдаче", validation_alias="id")  # Добавлено отсутствующее поле
    librarian_id: int = Field(..., description="ID библиотекаря")  # Исправлена опечатка
    borrow_date: datetime = Field(..., example="2023-01-01T00:00:00")
    return_date: Optional[datetime] = Field(None, example="2023-02-01T00:00:00")

class BorrowWithBook(BorrowBookResponse):
    book: Optional["ResponseBook"] = None
    reader: Optional["ResponseReader"] = None

class ShortBorrowResponse(BorrowBooksBase):
    record_id: int = Field(..., example=1, validation_alias="id")
    borrow_date: datetime = Field(..., example="2023-01-01T00:00:00")
    return_date: Optional[datetime] = Field(None, example="2023-02-01T00:00:00")

