from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from app.api.router import initialize_routes

app = Flask(__name__)
api = Api(app)


initialize_routes(api)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Library API (Flask Edition)",
        "description": "Лабораторна робота №5: Реалізація API на Flask-RESTful + Swagger",
        "version": "1.0.0"
    },
    "basePath": "/",
})

@app.route('/')
def index():
    return {"message": "Flask Library API is running! Go to /apidocs for Swagger"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)