from .book import ResponseBook, ShortBookResponse
from .borrow import BorrowBookResponse, ShortBorrowResponse, BorrowWithBook
from .reader import ShortReaderResponse, ResponseReader
from .librarian import ShortLibrarianResponse

__all__ = [
    "ResponseBook", "ShortBookResponse", 
    "BorrowBookResponse", "ShortBorrowResponse", 
    "ShortReaderResponse", "ShortLibrarianResponse",
    "BorrowWithBook"
]


BorrowWithBook.model_rebuild()