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

test_book_data = {
    "title": "И наказание",
    "author": "Фёдор Достоевский",
    "pub_year": 1866,
    "copies": 20
}


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
       
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database tables created")
        yield client
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("Database tables dropped")


@pytest.fixture(scope="session")
async def registered_librarian(async_client):
    response = await async_client.post("/librarian/register", json=test_user)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope="session")
async def auth_token(async_client, registered_librarian):
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = await async_client.post("/librarian/login", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]



@pytest.fixture(scope="session")
async def created_book(async_client, auth_token):
    """Фикстура для создания тестовой книги с автоматической очисткой"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.post(
        "/book",
        json=test_book_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    yield data
    
    try:
        await async_client.delete(
            f"/book/{data['book_id']}",
            headers=headers
        )
    except Exception as e:
        print(f"Ошибка при удалении тестовой книги: {e}")

@pytest.fixture(scope="session")
async def created_reader(async_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    reader_data = {
        "name": "Иван Иванов",
        "email": "reader@example.com"
    }
    response_reader = await async_client.post("/reader", json=reader_data, headers=headers)
    assert response_reader.status_code == 200

    reader_id = response_reader.json()['reader_id']
    return reader_id


@pytest.fixture(scope="session")
async def created_borrow(
    async_client, auth_token, 
    created_book, created_reader
):
    headers = {"Authorization": f"Bearer {auth_token}"}
    book_id = created_book["book_id"]
    response = await async_client.post(
        url="/borrow",
        json={
            "book_id": book_id,
            "reader_id": created_reader,
            "borrow_date": "2023-01-01",  #
            "return_date": "2023-02-01"   
        },
        headers=headers
    )
    if response.status_code != 200:
        print("Error creating borrow:", response.json())
        pytest.fail(f"Failed to create borrow: {response.json()}")
    
    data = response.json()
    return data