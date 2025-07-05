class BaseException(Exception):
    """Base Exception"""
    status_code: int = 500
    msg: str = "Server Error"

class NotFoundException(BaseException):
    status_code: int = 404
    msg: str = "Not found result"

class ConflictException(BaseException):
    status_code: int = 409
    msg: str = "Conflict Error"

class LimmitException(BaseException):
    status_code: int = 409
    msg: str = "Limited"

class UnauthorizedException(BaseException):
    status_code: int = 401
    msg: str = "User not authorize"

class ClientException(BaseException):
    status_code: int = 400
    msg: str = "Bad request"