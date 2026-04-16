from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.api.auth import oauth2_scheme  
from app.schemas.book import Book, BookCreate
from app.services.book_service import BookService
from app.repository.book_repo import BookRepository
from app.models.database import db

router = APIRouter(prefix="/books", tags=["Books"])

# Залежність для захисту ендпоінтів
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.get("sub")

def get_book_service():
    repository = BookRepository(db=db)
    return BookService(repository)

@router.get("/", response_model=List[Book])
async def get_all_books(
    current_user: str = Depends(get_current_user), # Захист
    service: BookService = Depends(get_book_service)
):
    return await service.get_books(limit=10, offset=0)

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    current_user: str = Depends(get_current_user), # Захист
    service: BookService = Depends(get_book_service)
):
    return await service.create_book(book_data)