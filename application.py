from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# setup our database with a table for books
# easiest way to do this is to use the python terminal
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# for sqlalchemy we use db.model class; it's going to inherit from db.model a bunch of functionality;
# that's how we can use this with sqlalchemy
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
    for book in books:
        book_data = {'name': book.name,'description': book.description}
        output.append(book_data)
    return {"books": "book data"}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.name, "description": book.description}