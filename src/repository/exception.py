class NotFoundException(Exception):
    """"""

class BookException(Exception):
    """Base exception for book opperations"""
    status_code: int = 500

class BookNotFound(BaseException):
    status_code: int = 404


class LibraryException(Exception):
    """Base exception for library operations"""
    status_code: int = 500

class NotFoundException(LibraryException):
    status_code = 404

class ConflictException(LibraryException):
    status_code = 409

class DataBaseErrorExceprion(LibraryException):
    status_code = 500

class UnauthorizedException(LibraryException):
    status_code: int = 401


class ReaderException(Exception):
    """Base exception for reader operations """
    status_code: int = 500

class ReaderNotFound(ReaderException):
    status_code: int = 404

class ReaderConflict(ReaderException):
    status_code: int = 400