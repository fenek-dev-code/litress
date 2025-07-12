import pytest


test_book_data = {
    "title": "Преступление и наказание",
    "author": "Фёдор Достоевский",
    "pub_year": 1866,
    "copies": 2
}

update_book_data = {
    "title": "Новое название",
    "author": "Новый автор",
    "pub_year": 2020,
    "copies": 10
}




@pytest.mark.asyncio
async def test_create_book_unauthorized(async_client):
    """Тест: нельзя создать книгу без авторизации"""
    response = await async_client.post("/book", json=test_book_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_book_success(async_client, auth_token):
    """Тест успешного создания книги"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.post(
        "/book",
        json=test_book_data,
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    required_fields = ["book_id", "created_at", "librarian_id"]
    for field in required_fields:
        assert field in data, f"Поле {field} отсутствует в ответе"
    
    for key in test_book_data:
        assert data[key] == test_book_data[key], f"Неверное значение для поля {key}"

@pytest.mark.asyncio
async def test_update_nonexistent_book(async_client, auth_token):
    """Тест: обновление несуществующей книги"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.patch(
        "/book/999999", 
        json=update_book_data,
        headers=headers
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_book_unauthorized(async_client, created_book):
    """Тест: нельзя обновить книгу без авторизации"""
    book_id = created_book["book_id"]
    response = await async_client.patch(f"/book/{book_id}", json=update_book_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_book_success(async_client, auth_token, created_book):
    """Тест успешного обновления книги"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    book_id = created_book["book_id"]
    
    response = await async_client.patch(
        f"/book/{book_id}",  
        json=update_book_data,
        headers=headers
    )
    
    assert response.status_code == 200
    updated_data = response.json()

    for key in update_book_data:
        assert updated_data[key] == update_book_data[key], f"Поле {key} не обновилось"
    
    assert updated_data["book_id"] == book_id
    assert "created_at" in updated_data

@pytest.mark.asyncio
async def test_delete_book_success(async_client, auth_token, created_book):
    """ Тест успешного удаления книги """
    headers = {"Authorization": f"Bearer {auth_token}"}
    book_id = created_book["book_id"]
    
    delete_response = await async_client.delete(
        f"/book/{book_id}",  
        headers=headers
    )
    assert delete_response.status_code == 200
    
    check_response = await async_client.get(
        f"/book/{book_id}",
        headers=headers
    )
    assert check_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_nonexistent_book(async_client, auth_token):
    """ Тест: удаление несуществующей книги """
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.delete(
        "/book/999999",  
        headers=headers
    )
    assert response.status_code == 404