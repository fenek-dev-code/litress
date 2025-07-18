from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from utils.auth_jwt import hash_password, verefy_passowrd

from .base import BaseRepository
from core.models.librarian import Librarian
from core.exceptions import (
    NotFoundError, ConflictBookError, ServerError
)

class LibrarianRepository(BaseRepository[Librarian]):

    async def create_librarian(self, name: str,  email: str, password: str):
        existing = await self.get_by_email(email)
        if existing:
            raise ConflictBookError(message=f"Читатель с тиким Email уже есть")
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
            existing = await self.session.get(Librarian, id)
            if not existing:
                raise NotFoundError(message=f"Библиотекарь {id} не найден")
            
            allowed_fields = {'name', 'email', 'password_hash'}
            password_hash = data.get('passowrd')
            if password_hash is not None:
                data['password_hash'] = password_hash

            for key, value in data.items():
                if hasattr(existing, key) and key in allowed_fields:
                    if value is not None:
                        setattr(existing, key, value)
            
            await self.session.flush()
            await self.session.commit()
            self.logger.info(f"Update Librarian: {id}")
            return existing
        except SQLAlchemyError as e:
            self.logger.error(f"Error during update, Librarian: {id} \nError[{e}]")
            raise ServerError

    async def get_with_readers(self, librarian_id: int):
        try:
            result = (await self.session.execute(
                select(Librarian)
                .where(Librarian.id == librarian_id)
                .options(selectinload(Librarian.readers))
            )).scalar_one_or_none()
            if not result:
                raise NotFoundError(message=f"Библиотекарь {id} не найден")
            return result
        
        except SQLAlchemyError:
            raise ServerError