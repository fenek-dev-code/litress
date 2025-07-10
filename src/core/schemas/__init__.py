from .book import ResponseBook, ShortBookResponse
from .borrow import BorrowBookResponse, ShortBorrowResponse, BorrowWithBookAndReader
from .reader import ShortReaderResponse, ResponseReader
from .librarian import ShortLibrarianResponse



BorrowWithBookAndReader.model_rebuild()