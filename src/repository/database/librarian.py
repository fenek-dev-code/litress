from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from utils.auth_jwt import hash_password, verefy_passowrd

from .base import BaseRepository
from core.models.librarian import Librarian
from repository.exception import NotFoundException, ConflictException, UnauthorizedException, DataBaseErrorExceprion

class LibrarianRepository(BaseRepository[Librarian]):

    async def create_librarian(self, librarian: Librarian):
        existing = await self.get_librarian_by_email(librarian.email)
        if existing:
            raise ConflictException()
        
        librarian.password_hash = hash_password(librarian.password_hash)
        
        async with self.session.begin():
            self.session.add(librarian)
            await self.session.flush()
            self.logger.info(f"Created librarian {librarian.id}")
            return librarian

    async def authenticate(self, email: str, password: str) -> Librarian:
        try:
            librarian = await self.get_librarian_by_email(email)
            if not verefy_passowrd(password, librarian.password_hash):
                raise UnauthorizedException("Invalid credentials") 
            return librarian
        except NotFoundException:
            raise UnauthorizedException("Invalid credentials")
        
    async def get_with_readers(self, librarian_id: int):
        try:
            result = (await self.session.execute(
                select(Librarian)
                .where(Librarian.id == librarian_id)
                .options(selectinload(Librarian.readers))
            )).scalar_one_or_none()
            if not result:
                raise NotFoundException
            return result
        
        except SQLAlchemyError:
            raise DataBaseErrorExceprion