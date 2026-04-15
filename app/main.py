from fastapi import FastAPI
from app.api.router import router as book_router
from app.models.database import engine, Base

app = FastAPI(title="Library API with Postgres")

# Цей блок створює таблиці в БД (якщо їх ще немає) при запуску
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(book_router)

@app.get("/")
def root():
    return {"message": "Library API is running in Docker!"}