from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from enum import Enum
from typing import Optional, Annotated

# Функція для конвертації ObjectId у рядок (щоб Pydantic не сварився)
PyObjectId = Annotated[str, BeforeValidator(str)]

class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int = Field(..., gt=0, lt=2100)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    # Змінюємо UUID на наш PyObjectId
    # Field(alias="_id") каже Pydantic брати дані з поля _id (як у Mongo)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Дозволяємо працювати і з id, і з _id
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "status": "available",
                "year": 1925
            }
        }
    )