from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.book_repo import BookRepository
from app.schemas.book import BookStatus, BookCreate

class BookService:
    def __init__(self, db: AsyncSession):
        # Передаємо db, яку отримали з роутера, прямо в репозиторій
        self.repository = BookRepository(db)

    async def get_books(
        self, 
        limit: int, 
        offset: int, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None
    ):
        return await self.repository.get_all(limit, offset, status, author)

    async def get_book_by_id(self, book_id: UUID):
        return await self.repository.get_by_id(book_id)

    async def create_book(self, book_data: BookCreate):
        return await self.repository.create(book_data)

    async def delete_book(self, book_id: UUID):
        await self.repository.delete(book_id)