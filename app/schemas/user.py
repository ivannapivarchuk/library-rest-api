from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)


class UserResponse(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str

    class Config:
        populate_by_name = True