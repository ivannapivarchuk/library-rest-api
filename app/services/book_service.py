from uuid import UUID
from typing import Optional, List
from app.repository.book_repo import BookRepository
from app.schemas.book import BookStatus

class BookService:
    def __init__(self):
        self.repository = BookRepository()

    async def get_books(
        self, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None,
        sort_by: Optional[str] = None
    ):
        books = await self.repository.get_all()
        
        # Фільтрація
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]
        
        # Сортування (title або year)
        if sort_by in ["title", "year"]:
            books = sorted(books, key=lambda x: x[sort_by])
            
        return books

    async def get_book_by_id(self, book_id: UUID):
        return await self.repository.get_by_id(book_id)

    async def create_book(self, book_data):
        return await self.repository.create(book_data)

    async def delete_book(self, book_id: UUID):
        return await self.repository.delete(book_id)