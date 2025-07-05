from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from utils.auth_jwt import hash_password, verefy_passowrd

from .base import BaseRepository
from core.models.librarian import Librarian
from repository import exception

class LibrarianRepository(BaseRepository[Librarian]):

    async def create_librarian(self, librarian: Librarian):
        existing = await self.get_librarian_by_email(librarian.email)
        if existing:
            raise exception.ConflictException
        
        librarian.password_hash = hash_password(librarian.password_hash)
        
        async with self.session.begin():
            self.session.add(librarian)
            await self.session.flush()
            self.logger.info(f"Created librarian {librarian.id}")
            return librarian

    async def authenticate(self, email: str, password: str) -> Librarian:
        librarian = await self.get_by_email(email=email)
        if not librarian:
            raise exception.ClientException
        if not verefy_passowrd(password, librarian.password_hash):
            raise exception.ClientException
        return librarian

        
    async def get_with_readers(self, librarian_id: int):
        try:
            result = (await self.session.execute(
                select(Librarian)
                .where(Librarian.id == librarian_id)
                .options(selectinload(Librarian.readers))
            )).scalar_one_or_none()
            if not result:
                raise exception.NotFoundException
            return result
        
        except SQLAlchemyError:
            raise exception.BaseException