from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(
            self, 
            message: str, 
            code: int = status.HTTP_404_NOT_FOUND
        ):
        super().__init__(
            status_code=code,
            detail=message
        )

class UnauthorizedError(NotFoundError):
    def __init__(self):
        super().__init__(
            message="Authentication required",
            code= status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ServerError(NotFoundError):
    def __init__(self, 
        message: str = "Server Error", 
        code = status.HTTP_404_NOT_FOUND
    ):
        super().__init__(message, code)


class BookLimitError(NotFoundError):
    def __init__(
            self, 
            message: str = "Не возможно арендовать более 3х книг", 
            code: int = status.HTTP_400_BAD_REQUEST 
        ):
        super().__init__(message, code)

class ConflictBookError(NotFoundError):
    def __init__(
        self, 
        message: str, 
        code = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, code)

class UserLogInError(NotFoundError):
    def __init__(
        self, 
        message: str = "Не верный логин или пароль", 
        code = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, code)