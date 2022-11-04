from app import db
from app.models.author import Author, Book
from flask import Blueprint, jsonify, make_response, request, abort

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

# helper functions - we can reuse this for multiple models
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = cls.query.get(model_id)
   
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
    return model

@authors_bp.route("", methods=["GET"], strict_slashes=False) #Here we are defining a route. This decorator (a decorator is a function that modifies another function) tells Python when to call this function
def get_all_authors():
    name_query = request.args.get("name") # we get None if not there
    limit_query = request.args.get("limit")

    author_query = Author.query

    if name_query:
        author_query = author_query.filter_by(name=name_query)
    if limit_query:
        author_query = author_query.filter_by(limit_query)

    authors = author_query.all()

    authors_response = [author.to_dict() for author in authors]
    return make_response(jsonify(authors_response), 200)

@authors_bp.route("", methods=["POST"], strict_slashes=False)
def create_author():
    request_body = request.get_json()
    new_author = Author.from_dict(request_body)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["POST"], strict_slashes=False)
def post_book_to_author(author_id):
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    new_book.author = author

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["GET"], strict_slashes=False) #Here we are defining a route. This decorator (a decorator is a function that modifies another function) tells Python when to call this function
def get_all_books_from_one_author(author_id):
    authors = validate_model(Author, author_id)
    book_response = [book.to_dict() for book in authors.books]
    return make_response(jsonify(book_response), 200)
