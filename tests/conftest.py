import pytest
from app import create_app #how you connect to your flask app from this file, specifically the create_app function
from app import db
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
    def client(app): #app is coming is coming from our ficture def app()
        return app.test_client()


