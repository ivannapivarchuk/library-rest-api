from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.auth import router as auth_router
from app.models.database import db # Переконайся, що тут ініціалізовано клієнт
from app.api.router import router as book_router  
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Дії при запуску: можна перевірити конект до бази
    print("Starting up: Connecting to MongoDB...")
    yield
    # Дії при вимкненні: закриття з'єднань
    print("Shutting down: Closing connections...")

app = FastAPI(
    title="Library API with Auth",
    description="API бібліотеки з JWT Auth та Refresh Token flow",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)

# Підключаємо роутер книг
app.include_router(book_router)

@app.get("/")
async def root():
    return {"message": "Welcome to protected Library API. Go to /docs for Swagger UI"}