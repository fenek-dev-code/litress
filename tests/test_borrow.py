import pytest 


@pytest.mark.asyncio
async def test_borrow_unauthorized(async_client):
    """Тест: неавторизованный доступ"""
    response = await async_client.post("/borrow", json={"book_id": 1, "reader_id": 1})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_borrow(async_client, created_borrow, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        url=f"/borrow/{created_borrow['record_id']}",
        headers=headers
    )
    assert response.status_code == 200
    data  = response.json()
    expected_fields = ["record_id", "librarian_id", "borrow_date", "return_date", "reader_id", "book_id"]
    for fild in expected_fields:
        assert fild in data
    assert isinstance(data["record_id"], int)
    assert isinstance(data["librarian_id"], int)
    assert isinstance(data["book_id"], int)

@pytest.mark.asyncio
async def test_get_borrow_unauthorize(async_client, created_borrow):
    """Тест: неавторизованный доступ"""
    response = await async_client.get(
        url=f"/borrow/{created_borrow['record_id']}",
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_nonexistent_borrow(async_client, auth_token):
    """Тест: не существоующий заказ"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get("/borrow/999999", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_borrow_invalid_data(async_client, auth_token):
    """Тест создания записи с невалидными данными"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await async_client.post(
        "/borrow",
        json={"book_id": 999999, "reader_id": 1},
        headers=headers
    )
    assert response.status_code == 404
    
    response = await async_client.post(
        "/borrow",
        json={"book_id": 1, "reader_id": 999999},
        headers=headers
    )
    assert response.status_code == 404
    
    response = await async_client.post(
        "/borrow",
        json={"book_id": 1},  
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_borrow_already_borrowed_book(async_client, auth_token, created_reader, created_book):
    """Тест: нельзя выдать уже выданную книгу"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await async_client.post(
        "/borrow",
        json={
            "book_id": created_book["book_id"],
            "reader_id": created_reader
        },
        headers=headers
    )
    assert response.status_code == 400
    assert "уже в аренде у читателя" in response.json()["detail"]


@pytest.mark.asyncio
async def test_return_borrow(async_client, auth_token, created_borrow):
    """Тест: возврат кинги"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response_book_old = await async_client.get(f"/book/{created_borrow["book_id"]}", headers=headers)
    assert response_book_old.status_code == 200

    response = await async_client.post(
        url="/borrow/return", 
        json={
            "book_id": created_borrow['book_id'],
            "reader_id": created_borrow['reader_id']
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["return_date"] is not None
    assert data["book_id"] == created_borrow["book_id"]
    assert data["reader_id"] == created_borrow["reader_id"]

    response_book_update = await async_client.get(f"/book/{created_borrow["book_id"]}", headers=headers)
    assert response_book_update.status_code == 200
    assert response_book_old.json()['copies'] < response_book_update.json()['copies']
    
@pytest.mark.asyncio
async def test_return_borrow_unauthorize(async_client):
    response = await async_client.post(
    url="/borrow/return", 
    json={
        "book_id": 1,
        "reader_id": 1
    }
    )
    assert response.status_code == 401