from uuid import UUID, uuid4
from app.models.storage import books_db
from app.schemas.book import BookCreate

class BookRepository:
    async def get_all(self):
        return books_db

    async def get_by_id(self, book_id: UUID):
        return next((book for book in books_db if book["id"] == book_id), None)

    async def create(self, book_data: BookCreate):
        new_book = book_data.model_dump()
        new_book["id"] = uuid4()
        books_db.append(new_book)
        return new_book

    async def delete(self, book_id: UUID):
        global books_db
        # Знаходимо індекс книги
        for i, book in enumerate(books_db):
            if book["id"] == book_id:
                return books_db.pop(i)
        return None