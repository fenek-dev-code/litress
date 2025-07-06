from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from repository.session import get_session
from core.service.librarian import LibrarianService
from core.service.book import BookService
from core.service.reader import ReaderService
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


OAuth_Bearer = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)
def currnet_user(
    token: str = Depends(OAuth_Bearer)
) -> TokenData:
    payload = decode_jwt(token=token)
    return TokenData(**payload)