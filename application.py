from flask import Flask, request
#import the SQLAlchemy class from the flask_sqlalchemy module
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# setup our database with a table for books
# easiest way to do this is to use the python terminal
#configure the database so we can connect to it.
#this creates an sqllite database called data.db..."in the same directory"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#db is an instance of the SQLAlchemy class and I'm passing in my flask app; not sure what
#I'm passing in though.
db = SQLAlchemy(app)

# for sqlalchemy we use db.model class; it's going to inherit from db.model a bunch of functionality;
# that's how we can use this with sqlalchemy
# this below code "defines the model"
class Book(db.Model):
    #define the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

# why is this over riding a method?
# is it because db.model class has a repr method?
# this will be invoked when we try to print out the drink in the list
    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'Hello, world'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    print(f"Books is {books}")
    for book in books:
        book_data = {'name': book.name,'description': book.description}
        output.append(book_data)
        print(f"Book data is {book_data}")
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.name, "description": book.description}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.json['name'], 
                description=request.json['description'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"Message": "Book deleted"}

