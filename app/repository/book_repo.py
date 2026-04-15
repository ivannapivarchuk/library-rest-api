from uuid import UUID
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book_model import BookModel
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self, 
        limit: int, 
        cursor: Optional[UUID] = None, 
        status=None, 
        author=None
    ):
        # 1. Починаємо запит і ОБОВ'ЯЗКОВО додаємо сортування.
        # Курсорна пагінація не працює без чіткого порядку (зазвичай за ID або часом створення).
        query = select(BookModel).order_by(BookModel.id).limit(limit)
        
        # 2. Якщо курсор передано, вибираємо тільки ті записи, де ID > нашого курсора
        if cursor:
            query = query.where(BookModel.id > cursor)
        
        # 3. Фільтрація залишається як була
        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author.ilike(f"%{author}%"))
            
        result = await self.session.execute(query)
        return result.scalars().all()

    # Решта методів (get_by_id, create, delete) залишаються БЕЗ змін
    async def get_by_id(self, book_id: UUID):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, book_data: BookCreate):
        new_book = BookModel(**book_data.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def delete(self, book_id: UUID):
        query = delete(BookModel).where(BookModel.id == book_id)
        await self.session.execute(query)
        await self.session.commit()