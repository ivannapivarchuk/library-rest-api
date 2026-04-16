from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional

from app.schemas.book import Book, BookCreate, BookStatus
from app.services.book_service import BookService
from app.repository.book_repo import BookRepository  # Імпортуємо репозиторій

router = APIRouter(prefix="/books", tags=["Books"])

# Функція для отримання сервісу (Dependency Injection)
def get_book_service():
    repository = BookRepository(db=db)
    return BookService(repository)

@router.get("/", response_model=List[Book])
async def get_all_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0), 
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    service: BookService = Depends(get_book_service) # Отримуємо сервіс через Depends
):
    # Тепер сервіс уже має в собі репозиторій і готовий до роботи
    return await service.get_books(limit=limit, offset=offset, status=status, author=author)

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    service: BookService = Depends(get_book_service)
):
    return await service.create_book(book_data)