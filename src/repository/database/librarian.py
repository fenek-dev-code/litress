from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from utils.auth_jwt import hash_password, verefy_passowrd

from .base import BaseRepository
from core.models.librarian import Librarian
from repository import exception

class LibrarianRepository(BaseRepository[Librarian]):

    async def create_librarian(self, name: str,  email: str, password: str):
        existing = await self.get_by_email(email)
        if existing:
            raise exception.ConflictException
        librarian = Librarian(
            name=name,
            email=email,
            password_hash=password
        )
        
        self.session.add(librarian)
        await self.session.commit()
        await self.session.refresh(librarian)
        self.logger.info(f"Created librarian {librarian.id}")
        return librarian
    
    async def update_librarian(self, id: int, data: dict):
        try:
            existing = await self.get(id)
            if not existing:
                raise exception.NotFoundException
            for key, value in data:
                if hasattr(existing, key):
                    setattr(existing, key, value)
            
            await self.session.refresh(existing)
            await self.session.commit()
            self.logger.info(f"Update Librarian: {id}")
            return existing
        except SQLAlchemyError as e:
            self.logger.error(f"Error during update, Librarian: {id} \nError[{e}]")
            raise exception.BaseException

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