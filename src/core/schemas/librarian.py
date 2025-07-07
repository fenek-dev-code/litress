from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from .reader import ShortReaderResponse

class BaseLibrarian(BaseModel):
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        example="Анна Петрова",
        description="Полное имя библиотекаря"
    )
    class Config:
        from_attributes  = True

class RegisterLibrarian(BaseLibrarian):
    email: EmailStr = Field(
        ..., 
        example="librarian@example.com",
        description="Рабочий email библиотекаря"
    )
    password: str = Field(
        ..., 
        min_length=8,
        example="SecureP@ss123",
        description="Пароль длиной не менее 8 символов"
    )

class LogInLibrarian(BaseModel):
    email: EmailStr = Field(
        ..., 
        example="librarian@example.com",
        description="Email, использованный при регистрации"
    )
    password: str = Field(
        ..., 
        example="SecureP@ss123",
        description="Пароль учетной записи"
    )

class LibrarianResponse(BaseLibrarian):
    id: int = Field(..., example=1, description="Уникальный идентификатор библиотекаря", validation_alias="id")
    email: EmailStr = Field(..., example="librarian@example.com")
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z")
    class Config:
        from_attributes = True 

class ShortLibrarianResponse(BaseLibrarian):
    id: int = Field(..., example=1, validation_alias="id")
    email: EmailStr = Field(..., example="librarian@example.com")
    
    

class UpdateLibrarian(BaseModel):
    name: Optional[str] = Field(
        None, 
        min_length=2, 
        max_length=50,
        example="Анна Иванова",
        description="Новое имя библиотекаря"
    )
    email: Optional[EmailStr] = Field(
        None,
        example="new.email@example.com",
        description="Новый рабочий email"
    )


class LibrarianWithReadersResponse(ShortLibrarianResponse):
    readers: List["ShortReaderResponse"] = Field( 
        default_factory=list,
        example=[{"id": 1, "name": "Иван Сидоров", "email": "reader@example.com"}],
        description="Список читателей, обслуженных библиотекарем"
    )
