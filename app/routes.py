from flask import Blueprint, jsonify, abort, make_response

books_bp = Blueprint("books", __name__, url_prefix="/books")

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Book 1", "A fantasy novel set in an imaginary world."),
#     Book(2, "Book 2", "A fantasy novel set in an imaginary world."),
#     Book(3, "Book 3", "A fantasy novel set in an imaginary world.")
# ] 

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except: 
#         abort(make_response({"message": f"book {book_id} was invalid"}, 400)) # using abort instead of return so it doesn't continue on with our code in specific_book, abort expects a respoonse object so we need to use make_response to return an object
#     for book in books:
#         if book.id == book_id:
#             return book
#     abort(make_response({"message": f"book {book_id} was not found"}, 404))


# @books_bp.route("/<book_id>", methods=["GET"])
# def specific_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#             }


# @books_bp.route("", methods=["GET"])
# def books_list():
#     books_list = []
#     for book in books:
#         books_list.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_list), 200 # makes a Response object, used when returning a list

