from pydantic import BaseModel, EmailStr, Field, conlist
from typing import List, Optional
from datetime import datetime

from .book import ResponseBook

class BaseReader(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Иван Иванов")
    email: EmailStr = Field(..., example="reader@example.com")

class CreateReader(BaseReader):
    pass

class ResponseReader(BaseReader):
    reader_id: int = Field(..., example=42)
    librarian_id: Optional[int] = Field(None, example=1)  
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z")
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() 
        }


class UpdateReader(BaseModel):

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


class ShortReaderResponse(BaseModel):
    reader_id: int
    name: str

class ReaderWithRecordsResponse(BaseModel):
    id: int
    name: str
    email: str
    borrow_records: List["BorrowRecordResponse"] = []  