import pytest


@pytest.mark.asyncio
async def test_register(async_client):
    """Тест регистрации библиотекаря с проверкой всех полей ответа"""
    user_data = {
        "name": "Анна Петрова",
        "email": "youemail@example.com",
        "password": "SecureP@ss123"
    }
    
    response = await async_client.post(
        "/librarian/register",
        json=user_data
    )
    assert response.status_code == 200
    
    data = response.json()
    expected_fields = ["id", "name", "email", "created_at"]
    for field in expected_fields:
        assert field in data, f"Поле {field} отсутствует в ответе"
    
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert isinstance(data["id"], int)
    
    sensitive_fields = ["password", "password_hash"]
    for field in sensitive_fields:
        assert field not in data, f"Поле {field} не должно возвращаться в ответе"

@pytest.mark.asyncio
async def test_login(async_client, registered_librarian):
    """Тест входа библиотекаря с проверкой токена"""
    login_data = {
        "email": registered_librarian.get("email", "testemail@example.com"),
        "password": registered_librarian.get("passowrd", "SecureP@ss123")
    }
    
    response = await async_client.post(
        "/librarian/login",
        json=login_data
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20  
    
    
    return data["access_token"]

@pytest.mark.asyncio
async def test_get_me_unauthenticated(async_client):
    """Тест доступа к профилю без аутентификации"""
    response = await async_client.get("/librarian")
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_get_me_authenticated(async_client, auth_token):
    """Тест получения профиля с аутентификацией"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        "/librarian",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "name" in data

@pytest.mark.asyncio
async def test_update_profile(async_client, auth_token):
    """Тест обновления профиля"""
    update_data = {
        "name": "Анна Иванова",
        "email": "new.email@example.com",
        "password": "SecureP@ss123"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await async_client.patch(
        "/librarian",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]



