from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional

class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int