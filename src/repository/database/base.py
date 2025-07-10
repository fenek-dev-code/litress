from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Generic, TypeVar
import logging


ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get(self, id: int) -> ModelType | None:
        return await self.session.get(self.model, id)
    
    async def get_by_email(self, email: str) -> ModelType | None:
        result = (await self.session.execute(
            select(self.model).where(self.model.email == email)
        )).scalar_one_or_none()
        return result 
    
    async def delete(self, id: int):
        async with self.session.begin():
            result = await self.session.execute(
                delete(self.model).where(self.model.id == id)
            )
            if result.rowcount == 0:
                raise False
            return True