from app import db
from app.models.book import Book

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship("Book", back_populates="author") #author table

    def to_dict(self):
        return (dict(
            id=self.id,
            name=self.name)
            )