from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from uuid import UUID, uuid4
from app.models.database import Base

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(default="available")
    year: Mapped[int] = mapped_column(Integer)