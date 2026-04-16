from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("books")

    async def get_all(self, limit: int, offset: int, status: Optional[str] = None, author: Optional[str] = None):
        filters = {}
        if status:
            filters["status"] = status
        if author:
            filters["author"] = {"$regex": author, "$options": "i"}

        cursor = self.collection.find(filters).skip(offset).limit(limit)
        books = await cursor.to_list(length=limit)
        
        # Конвертуємо _id з ObjectId в рядок для кожного документа
        for book in books:
            book["id"] = str(book.pop("_id"))
        return books

    async def create(self, book_data: BookCreate):
        book_dict = book_data.model_dump()
        result = await self.collection.insert_one(book_dict)
        # Додаємо id у відповідь, щоб фронтенд знав ID створеної книги
        book_dict["id"] = str(result.inserted_id)
        return book_dict