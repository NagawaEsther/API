
from authors_app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    #image = db.Column(db.BLOB, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(10), nullable=False, default='UGX')
    pages = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(30), nullable=True, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))


    def __init__(self, title, description, price, price_unit, pages, publication_date, isbn, genre, user_id, company_id,image=None):
        self.title = title
        self.description = description
        self.price = price
        self.price_unit = price_unit
        self.pages = pages
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre
        self.user_id = user_id
        self.company_id=company_id
        #self.image = image

    def __repr__(self):
        return f'<Book {self.title}>'
