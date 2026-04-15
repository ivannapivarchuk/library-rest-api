from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# URL для підключення (db — це буде ім'я сервісу в Docker)
DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/library"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# Залежність для отримання сесії БД в ендпоінти
async def get_db():
    async with SessionLocal() as session:
        yield session