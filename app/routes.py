from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort


books_bp = Blueprint("books", __name__, url_prefix="/books")

'''
For a little more flexibility, we could choose to use "/" as the route path and include the keyword argument strict_slashes=False. This tells the route to treat a URI the same whether or not it ends in /. Accepting either variation can make using our API a little easier for our clients.
'''

'''
the following function will execute whenever a matching HTTP request is received
We use the request object to get information about the HTTP request. We want to get the request's JSON body, so we use request.get_json(). This method "Pythonifies" the JSON HTTP request body by converting it to a Python dictionary.
'''
#helper functions
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({f"message": "Book {book_id} is invalid"}, 400))

    book = Book.query.get(book_id)
   
    if not book:
        abort(make_response({f"message": "Book {book_id} does not exist"}, 404))
    return book 



@books_bp.route("", methods=["GET"]) #Here we are defining a route. This decorator (a decorator is a function that modifies another function) tells Python when to call this function
def get_all_books():
    books = Book.query.all() # returns a list of book instances
    books_response = [book.to_dict() for book in books]
    return jsonify(books_response), 200

@books_bp.route("/<book_id>", methods=["GET"])
def get_one_book(book_id):
    book = validate_book(book_id)
    return book.to_dict()

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

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    try:
        book.title = request_body["title"]
        book.description = request_body["description"]
    except:
        abort(make_response({f"message": "You must enter a title AND a description"}, 400))

    db.session.commit()
    return make_response(f"Book {book.id} successfully updated", 200)
