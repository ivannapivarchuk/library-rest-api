import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

# Тестуємо створення книги
@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books/", json={
            "title": "Tale of Two Cities",
            "author": "Charles Dickens",
            "description": "A classic novel",
            "status": "available",
            "year": 1859
        })
    assert response.status_code == 201
    assert response.json()["title"] == "Tale of Two Cities"

# Тестуємо отримання списку книг
@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Тестуємо ідемпотентне видалення
@pytest.mark.asyncio
async def test_delete_book_idempotent():
    fake_id = "550e8400-e29b-41d4-a716-446655440000"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(f"/books/{fake_id}")
    # Навіть якщо книги немає, має повернути 204 (успіх без контенту)
    assert response.status_code == 204