from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request


books_bp = Blueprint("books", __name__, url_prefix="/books")

'''
For a little more flexibility, we could choose to use "/" as the route path and include the keyword argument strict_slashes=False. This tells the route to treat a URI the same whether or not it ends in /. Accepting either variation can make using our API a little easier for our clients.
'''

'''
the following function will execute whenever a matching HTTP request is received
We use the request object to get information about the HTTP request. We want to get the request's JSON body, so we use request.get_json(). This method "Pythonifies" the JSON HTTP request body by converting it to a Python dictionary.
'''
@books_bp.route("", methods=["GET"]) #Here we are defining a route. This decorator (a decorator is a function that modifies another function) tells Python when to call this function
def get_all_books():
    books = Book.query.all() # returns a list of book instances
    books_response = [book.to_dict() for book in books]
    return jsonify(books_response), 200

@books_bp.route("", methods=["POST"])
def post_book():
    request_body = request.get_json()
    #create an instance of Book
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])
    #the database's way of collecting changes that need to be made, here we are saying we want the database to add a new book and then commit the collected changes
    db.session.add(new_book)
    db.session.commit()
    # we want to return a response object from Flask endpoint functions
    return make_response(f"Book {new_book.title} successfully created", 201)


