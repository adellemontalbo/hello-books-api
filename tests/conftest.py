import pytest
from app import create_app #how you connect to your flask app from this file, specifically the create_app function
from app import db
from app.models.book import Book
from flask.signals import request_finished

@pytest.fixture
def app():
    app = create_app({"TESTING": True}) #make an instance of the the create_app function, this is listening for our test database

    @request_finished.connect_via(app) #make sure that with every request, when it's finished, it clears out temporary data
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context(): #within the context of our app, (which is looking at the test database), we want to use this context and generate a new start to our dtabase
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all() #within this context, clear out the data we messed with

@pytest.fixture #creating a dummy client to test our CRUD
def client(app): #app is coming from our app fixture
    return app.test_client()


@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                      description="watr 4evr")
    mountain_book = Book(title="Mountain Book",
                         description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()

