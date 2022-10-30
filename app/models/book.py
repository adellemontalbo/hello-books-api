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

    def to_dict(self):
        return (dict(
            id=self.id,
            title=self.title,
            description=self.description)
            )