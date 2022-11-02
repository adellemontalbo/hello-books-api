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
#helper functions - we can reuse this for multiple models
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = cls.query.get(model_id)
   
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
    return model

@books_bp.route("", methods=["GET"]) #Here we are defining a route. This decorator (a decorator is a function that modifies another function) tells Python when to call this function
def get_all_books():
    title_query = request.args.get("title") # we get None if not there
    description_query = request.args.get("description")
    limit_query = request.args.get("limit")

    book_query = Book.query

    if title_query:
        book_query = book_query.filter_by(title=title_query)
    if description_query:
        description_query = book_query.filter_by(description=description_query)
    if limit_query:
        book_query = book_query.filter_by(limit_query)

    books = book_query.all()

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response), 200


@books_bp.route("/<book_id>", methods=["GET"])
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return jsonify(book.to_dict()), 200


@books_bp.route("", methods=["POST"])
def post_book():
    request_body = request.get_json()
    #create an instance of Book
    new_book = Book.from_dict(request_body)
    #the database's way of collecting changes that need to be made, here we are saying we want the database to add a new book and then commit the collected changes
    db.session.add(new_book)
    db.session.commit()
    # we want to return a response object from Flask endpoint functions
    return make_response(f"Book {new_book.title} successfully created", 201)


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    
    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()
    return make_response(f"Book {book.id} successfully updated", 200)
    

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return make_response(f"Book {book.id} successfully deleted", 200)
    
