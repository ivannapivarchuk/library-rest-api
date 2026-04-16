from typing import List, Optional
from app.repository.book_repo import BookRepository
from app.schemas.book import BookCreate, Book

class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def create_book(self, book_data: BookCreate) -> Book:
        # Перетворюємо Pydantic модель у словник для MongoDB
        book_dict = book_data.model_dump()
        return await self.repository.create(book_dict)

    async def get_books(self, limit: int, offset: int) -> List[Book]:
        return await self.repository.get_all(limit, offset)

    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return await self.repository.get_by_id(book_id)

    async def update_book(self, book_id: str, book_data: BookCreate) -> Optional[Book]:
        return await self.repository.update(book_id, book_data.model_dump())

    async def delete_book(self, book_id: str) -> bool:
        return await self.repository.delete(book_id)