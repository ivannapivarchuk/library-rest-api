from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.schemas.book import Book, BookCreate, BookStatus
from app.services.book_service import BookService
from app.models.database import get_db  # Імпортуємо функцію підключення до БД

router = APIRouter(prefix="/books", tags=["Books"])

# ВИДАЛИЛИ: service = BookService() - тепер ми створюємо його всередині функцій

@router.get("/", response_model=List[Book])
async def get_all_books(
    limit: int = Query(10, ge=1, le=100), # Пагінація: скільки взяти
    offset: int = Query(0, ge=0),         # Пагінація: скільки пропустити
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)    # Отримуємо сесію БД
):
    service = BookService(db) # Створюємо сервіс з базою
    return await service.get_books(limit, offset, status, author)

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.create_book(book_in)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    await service.delete_book(book_id)
    return None