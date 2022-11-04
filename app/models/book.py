from app import db

'''
from app, import db
We define a new class and name it after our model, usually singular
By default, SQLAlchemy will use the lowercase version of this class name as the name of the table it will create.
In model definitions, if we don't like the default name that SQLAlchemy picks we can specify a different name for the table, using the __tablename__ property. 
'''
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="books")

    @classmethod #belongs to the class as a whole, not instance. cls is a variable that refers to a class object
    def from_dict(cls, data_dict): #it passes in the class itself, not self (instance)
        return cls(title=data_dict["title"],
            description=data_dict["description"])

    def to_dict(self):
        return (dict(
            id=self.id,
            title=self.title,
            description=self.description)
            )