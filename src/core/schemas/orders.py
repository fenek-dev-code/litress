from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BorrowRecordBase(BaseModel):
    book_id: int = Field(..., example=1, description="ID книги")
    reader_id: int = Field(..., example=1, description="ID читателя")

class BorrowRecordCreate(BorrowRecordBase):
    pass  # Можно добавить дополнительные поля при необходимости

class BorrowRecordReturn(BaseModel):
    record_id: int = Field(..., example=1, description="ID записи о выдаче")

class BorrowRecordResponse(BorrowRecordBase):
    librarian_id: int = Field(..., description="ID Библиотекоря который создал зака")
    borrow_date: datetime = Field(...,)
    return_date: datetime | None = None

class BorrowRecordFilter(BaseModel):
    """Параметры фильтрации для поиска записей"""
    book_id: Optional[int] = None
    reader_id: Optional[int] = None
    is_active: Optional[bool] = Field(
        None, 
        description="True - только активные, False - только возвращенные, None - все"
    )
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

