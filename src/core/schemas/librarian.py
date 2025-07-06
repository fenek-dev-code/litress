from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

class BaseLibrarian(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Анна Петрова")

class RegisterLibrarian(BaseLibrarian):
    email: EmailStr = Field(..., example="librarian@example.com")
    password: str = Field(..., min_length=8)

class LogInLibrarian(BaseModel):
    email: EmailStr = Field(..., example="librarian@example.com")
    password: str = Field(..., example="Str0ngP@ss")

class ResponseLibrarian(BaseLibrarian):
    id: int = Field(..., example=1)
    email: EmailStr = Field(..., example="librarian@example.com")
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z")
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() 
        }

class ShortLibrarianResponse(BaseLibrarian):
    id: int
    email: EmailStr

class UpdateLibrarian(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None

class ResponseLibrarianWithReaders(ShortLibrarianResponse):
    readers: List["ShortReaderResponse"] = Field(default=[], examples=[])
