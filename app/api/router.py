from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.schemas.book import Book, BookCreate, BookStatus
from app.services.book_service import BookService
from app.models.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[Book])
async def get_all_books(
    limit: int = Query(10, ge=1, le=100),
    # ЗАМІНИЛИ offset на cursor
    cursor: Optional[UUID] = Query(None, description="ID останньої отриманої книги для пагінації"),
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    service = BookService(db)
    # Передаємо cursor замість offset
    return await service.get_books(limit, cursor, status, author)

# Решта методів (get_book, create_book, delete_book) залишаються без змін
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