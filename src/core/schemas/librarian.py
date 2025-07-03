from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime
from typing import List, Optional

from .reader import ResponseReader

class BaseLibrarian(BaseModel):
    """
    Базовая модель библиотекаря
    
    Attributes:
        name: Полное имя (2-50 символов)
    """
    name: str = Field(..., min_length=2, max_length=50, example="Анна Петрова")

class RegisterLibrarian(BaseLibrarian):
    """
    Модель регистрации библиотекаря
    
    Example:
        ```json
        {
            "name": "Иван Иванов",
            "email": "librarian@example.com",
            "password": "Str0ngP@ss"
        }
        ```
    """
    email: EmailStr = Field(..., example="librarian@example.com")
    password: str = Field(..., min_length=8)

class LogInLibrarian(BaseModel):
    """
    Модель входа библиотекаря
    
    Example:
        ```json
        {
            "email": "librarian@example.com",
            "password": "Str0ngP@ss"
        }
        ```
    """
    email: EmailStr = Field(..., example="librarian@example.com")
    password: str = Field(..., example="Str0ngP@ss")

class ResponseLibrarian(BaseLibrarian):
    """
    Модель ответа с данными библиотекаря
    
    Attributes:
        id: Уникальный идентификатор
        created_at: Дата регистрации
        readers: Список прикреплённых читателей
    """
    id: int = Field(..., example=1)
    email: EmailStr = Field(..., example="librarian@example.com")
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z")
    readers: List[ResponseReader] = Field(default=[], example=[])

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Правильная сериализация даты
        }

class ShortLibrarianResponse(BaseLibrarian):
    """
    Сокращенная модель библиотекаря для списков и публичных ответов.
    Содержит только базовую идентификационную информацию.
    
    Attributes:
        id: Уникальный идентификатор библиотекаря в системе
        email: Контактный email (валидируется на корректность формата)
        name: Полное имя (наследуется из BaseLibrarian, 2-50 символов)
    
    Использование:
    - Возвращается в списках библиотекарей
    - Используется в публичных API-ответах
    - Не содержит конфиденциальных данных (паролей и т.д.)
    """
    id: int
    email: EmailStr

class UpdateLibrarian(BaseModel):
    """
    Модель для частичного обновления данных библиотекаря.
    Все поля опциональны - обновляются только переданные значения.
    
    Особенности:
    - Поддерживает PATCH-запросы
    - None означает "не изменять поле"
    - Сохраняет валидацию из BaseLibrarian
    
    Example PATCH-запрос:
    ```json
    {
        "name": "Новое имя",
        "email": "new@example.com"
    }
    ```
    """
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None


class LibrarianTokenResponse(BaseModel):
    """
    Модель ответа с JWT-токеном после успешной аутентификации.
    Соответствует стандарту OAuth 2.0.
    
    Attributes:
        access_token: Подписанный JWT-токен для авторизации
        token_type: Тип токена (всегда "bearer")
    
    Security:
    - Токен должен передаваться в заголовке Authorization
    - Срок жизни токена определяется сервером
    
    Example:
    ```json
    {
        "access_token": "eyJhbGciOi...",
        "token_type": "bearer"
    }
    ```
    """
    access_token: str
    token_type: str = "bearer"

class LibrarianTokenData(BaseModel):
    id: int | None = None
    role: str | None = None