from fastapi import FastAPI
from settings import config
from api.enpoints import main_router
from contextlib import asynccontextmanager
from repository.session import engine
from core.models.base import Base
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Data Table is Create")
    yield 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Data Table is drop")

app = FastAPI(
    lifespan=lifespan,
    debug=True,
    title="BookService",
    description="Book borrow records service!"
)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=config.server.host,
        port=config.server.port
    )
