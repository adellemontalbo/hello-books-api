from flask import Blueprint, jsonify

hello_world_bp = Blueprint("hello_world", __name__)
books_bp = Blueprint("books", __name__, url_prefix="/books")

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Book 1", "A fantasy novel set in an imaginary world."),
    Book(2, "Book 2", "A fantasy novel set in an imaginary world."),
    Book(3, "Book 3", "A fantasy novel set in an imaginary world.")
] 

@books_bp.route("/<book_id>", methods=["GET"])
def specific_book(book_id):
    try:
        book_id = int(book_id)
    except: 
        return {"message": f"book {book_id} was invalid"}, 400
    for book in books:
        if book.id == book_id:
            return {
                "id": book.id,
                "title": book.title,
                "description": book.description
                    }
    return {"message": f"book {book_id} was not found"}, 404

@books_bp.route("", methods=["GET"])
def books_list():
    books_list = []
    for book in books:
        books_list.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_list), 200 # makes a Response object, used when returning a list


@hello_world_bp.route("/hello/JSON", methods=["GET"])
def hello_JSON():
    return {
        "name": "JSON SURE",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"],
    }, 200


@hello_world_bp.route("/hello-world", methods=["GET"])
def hello_world():
    my_response_body = "Hello, World!"
    return my_response_body, 201
