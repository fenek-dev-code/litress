from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from core.exceptions import UnauthorizedError, ServerError
from repository.session import get_session
from core.service.librarian import LibrarianService
from core.service.book import BookService
from core.service.reader import ReaderService
from core.service.borrow import BorrowService
from core.schemas.token import TokenData
from utils.auth_jwt import decode_jwt


def librarian_service(
    session: AsyncSession = Depends(get_session)
):
    return LibrarianService(session=session)

def book_service(
    session: AsyncSession = Depends(get_session)
):
    return BookService(session=session)

def reader_service(
    session: AsyncSession = Depends(get_session)
):
    return ReaderService(session=session)

def borrow_service(
    session: AsyncSession = Depends(get_session)
):
    return BorrowService(session=session)

OAuth_Bearer = OAuth2PasswordBearer(
    tokenUrl="librarian/token"
)
async def currnet_user(
    token_str: str = Depends(OAuth_Bearer)
) -> TokenData:
    try:
        payload = decode_jwt(token=token_str)
        token = TokenData(**payload)
        return token
    
    except ValueError:
        raise UnauthorizedError
    except:
        raise ServerError 
    