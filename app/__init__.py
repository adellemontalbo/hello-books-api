from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__) #this refers to the name of the current file, it tells Python to turn this into a flask application

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book

    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app

'''
Flask - a Python framework, a collection of libraries that someone else wrote and a set of convention for doing things. It makes it easier for us to do things we want to do with our app 
'''