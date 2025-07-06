from pydantic import BaseModel, Field, conint
from datetime import datetime
from typing import Optional

class BaseBook(BaseModel):
    """
    Базовая модель книги с основной валидацией полей.
    Используется как родительский класс для других моделей книги.
    
    Attributes:
        title: Название книги (обязательное, 2-200 символов)
        author: Автор (обязательное, 2-100 символов)
        pub_year: Опциональный год публикации (1800-текущий год)
        copies: Количество копий в библиотеке (по умолчанию 1, диапазон 1-1000)
    """
    title: str = Field(..., min_length=2, max_length=200, example="Преступление и наказание")
    author: str = Field(..., min_length=2, max_length=100, example="Фёдор Достоевский")
    pub_year: Optional[conint(ge=1800, le=datetime.now().year)] = Field( # type: ignore
        None, 
        example=1866,
        description="Год публикации (от 1800 до текущего года)"
    )
    copies: conint(ge=1, le=1000) = Field( # type: ignore
        default=1,
        example=5,
        description="Количество копий в библиотеке (1-1000)"
    )

class CreateBook(BaseBook):
    """
    Модель для создания новой книги через API.
    Наследует все поля BaseBook без изменений.
    
    Использование:
    - Отправляется в POST-запросе при добавлении новой книги
    - Все поля проходят валидацию согласно правилам BaseBook
    
    Example JSON:
    ```json
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "pub_year": 1967,
        "copies": 3
    }
    ```
    """
    pass

class ResponseBook(BaseBook):
    """
    Модель для возврата данных о книге в API-ответах.
    Расширяет BaseBook, добавляя служебные поля.
    
    Attributes:
        book_id: Уникальный идентификатор книги в системе
        librarian_id: ID библиотекаря, добавившего книгу
        created_at: Дата и время добавления записи (автоматически)
    
    Note:
    - Поля наследуются из BaseBook с той же валидацией
    - Дата автоматически форматируется в ISO-формат при сериализации
    """
    book_id: int = Field(..., example=42)
    librarian_id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-01-15T10:30:00Z")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Для корректной сериализации в JSON
        }

class ShortBookResponse(BaseModel):
    """
    Упрощенная модель книги для списков и поиска.
    Содержит только базовые идентификационные данные.
    
    Использование:
    - Возвращается в списках книг
    - Используется в сокращенных представлениях
    - Оптимизирована для массовой загрузки
    
    Fields:
        book_id: Уникальный идентификатор
        title: Название книги
        author: Автор
    """
    book_id: int = Field(..., example=1)
    title: str = Field(..., example="1984")
    author: str = Field(..., example="Джордж Оруэлл")

class UpdateBook(BaseModel):
    """
    Модель для обновления данных книги.
    Все поля опциональны - обновляются только переданные значения.
    
    Особенности:
    - Поддерживает частичное обновление
    - Сохраняет те же правила валидации, что и BaseBook
    - None означает "не изменять это поле"
    
    Example PATCH-запроса:
    ```json
    {
        "title": "Новое название",
        "copies": 10
    }
    ```
    """
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    author: Optional[str] = Field(None, min_length=2, max_length=100)
    pub_year: Optional[int] = Field(None, ge=1800, le=datetime.now().year)
    copies: Optional[int] = Field(None, ge=1, le=1000)

class BookSearchFilters(BaseModel):
    """
    Параметры фильтрации для поиска книг.
    Поддерживает поиск по диапазонам и частичным совпадениям.
    
    Особенности:
    - Все параметры объединяются через AND
    - Пустые значения игнорируются
    - Подходит для GET-запросов
    
    Example:
    ```json
    {
        "author": "Достоевский",
        "year_from": 1850,
        "year_to": 1900
    }
    ```
    """
    title: Optional[str] = None
    author: Optional[str] = None
    year_from: Optional[int] = Field(None, ge=1800)
    year_to: Optional[int] = Field(None, le=datetime.now().year)