from flask import request
from flask_restful import Resource
from app.repository.book_repo import BookRepository
from app.models.database import db

repo = BookRepository(db)

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Дані книги
        """
        
        return {"id": book_id, "title": "Example Book"}, 200

class BookListResource(Resource):
    def get(self):
        """
        Отримати список усіх книг
        ---
        responses:
          200:
            description: Список книг
        """
        
        return {"books": []}, 200