from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from settings import config
from typing import AsyncGenerator

engine = create_async_engine(
    url=config.db.url,
    echo=config.db.echo,
    max_overflow=config.db.max_overflow,
    pool_pre_ping=config.db.pool_pre_ping,
    pool_recycle=config.db.pool_recycle
)

sessioon_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessioon_factory() as session:
        yield session