import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app  
from src.core.models.base import Base
from repository.session import engine

test_user = {
    "name": "Анна Петрова",
    "email": "testemail@example.com",
    "password": "SecureP@ss123"
}


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        # Создаем таблицы перед всеми тестами
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database tables created")
        yield client
        # Удаляем таблицы после всех тестов
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("Database tables dropped")


@pytest.fixture
async def registered_librarian(async_client):
    response = await async_client.post("/librarian/register", json=test_user)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
async def auth_token(async_client):
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = await async_client.post("/librarian/login", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]
