import asyncio
from flask import request
from flask_restful import Resource
from app.repository.book_repo import BookRepository
from app.models.database import db
from app.schemas.book import BookCreate

# Створюємо репозиторій
repo = BookRepository(db=db)

# Допоміжна функція для запуску асинхронного коду в синхронному Flask
def run_async(coro):
    return asyncio.run(coro)

class BookListResource(Resource):
    def get(self):
        """
        Отримати список усіх книг
        ---
        tags:
          - Books
        parameters:
          - name: limit
            in: query
            type: integer
            default: 10
          - name: offset
            in: query
            type: integer
            default: 0
          - name: status
            in: query
            type: string
          - name: author
            in: query
            type: string
        responses:
          200:
            description: Список книг успішно отримано
        """
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        status = request.args.get('status')
        author = request.args.get('author')

        books = run_async(repo.get_all(limit=limit, offset=offset, status=status, author=author))
        return books, 200

    def post(self):
        """
        Створити нову книгу
        ---
        tags:
          - Books
        parameters:
          - name: body
            in: body
            required: true
            schema:
              required:
                - title
                - author
                - year
              properties:
                title:
                  type: string
                  example: "Кобзар"
                author:
                  type: string
                  example: "Тарас Шевченко"
                year:
                  type: integer
                  example: 1840
                description:
                  type: string
                  example: "Збірка поетичних творів"
                status:
                  type: string
                  default: "available"
        responses:
          201:
            description: Книга успішно створена
          400:
            description: Помилка валідації даних
        """
        data = request.get_json()
        if not data:
            return {"error": "Немає даних у запиті"}, 400

        try:
            # Валідація через Pydantic схему
            book_data = BookCreate(**data)
            new_book = run_async(repo.create(book_data))
            return new_book, 201
        except Exception as e:
            return {"error": str(e)}, 400

def initialize_routes(api):
    # Реєструємо ресурс. Endpoint допомагає Swagger ідентифікувати шлях
    api.add_resource(BookListResource, '/api/books', endpoint='books')