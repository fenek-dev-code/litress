from fastapi import Depends, HTTPException
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
async def currnet_user(
    token_str: str = Depends(OAuth_Bearer)
) -> TokenData:
    try:
        payload = decode_jwt(token=token_str)
        token = TokenData(**payload)
        return token
    
    except ValueError as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )