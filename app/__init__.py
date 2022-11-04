from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() #This built-in module provides a way to read environment variables

def create_app(test_config=None):
    app = Flask(__name__) #this refers to the name of the current file, it tells Python to turn this into a flask application
   
    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)

    #Import models here
    from app.models.book import Book
    from app.models.author import Author

    #Register Blueprints here
    from .routes import books_bp
    from .author_routes import authors_bp
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)

    return app

'''
Flask - a Python framework, a collection of libraries that someone else wrote and a set of convention for doing things. It makes it easier for us to do things we want to do with our app 
'''