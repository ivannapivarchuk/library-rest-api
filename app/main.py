from fastapi import FastAPI
from app.api.router import router as book_router

# Назва може бути будь-якою, але залиш "Library API"
app = FastAPI(title="Library API with MongoDB")

# Видаляємо блок startup з engine.begin(), бо в Mongo не треба створювати таблиці!
# MongoDB створить базу і колекції автоматично при першому записі.

app.include_router(book_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Library API is running with MongoDB in Docker!"}