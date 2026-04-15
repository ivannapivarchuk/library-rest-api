from fastapi import FastAPI
from app.api.router import router as book_router

app = FastAPI(title="Library API")

# Підключаємо наш роутер
app.include_router(book_router)

@app.get("/")
def root():
    return {"message": "Welcome to Library API. Go to /docs for Swagger UI"}