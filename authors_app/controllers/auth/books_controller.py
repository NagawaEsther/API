from flask import Blueprint, request, jsonify
from authors_app.models.books import Book
from authors_app import db
from flask_jwt_extended import jwt_required,get_jwt_identity

book = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book.route('/register', methods=['POST'])
def register_book():
    try:
        # Extracting request data
        title = request.json.get('title')
        description = request.json.get('description')
        price = request.json.get('price')
        price_unit = request.json.get('price_unit')
        pages = request.json.get('pages')
        publication_date = request.json.get('publication_date')
        isbn = request.json.get('isbn')
        genre = request.json.get('genre')
        user_id = request.json.get('user_id')
        company_id=request.json.get('company_id')
        #image=request.json.get('user_image')
     

        # Basic input validation
        if not all([title, description, price, price_unit, pages, publication_date, isbn, genre, user_id,company_id]):
            return jsonify({"error": 'All fields are required'}), 400

        # Check if 'image' field is provided
        #if image is None:
            #return jsonify({"error": 'Image is required'}), 400

        # Creating a new book
        new_book = Book(
            title=title,
            description=description,
            #image=image,
            price=float(price),
            price_unit=price_unit,
            pages=int(pages),
            publication_date=publication_date,
            isbn=isbn,
            genre=genre,
            user_id=int(user_id),
            company_id=int(company_id),
        
        )

        # Adding and committing to the database
        db.session.add(new_book)
        db.session.commit()

        # Return book details in response
        book_details = {
            'id': new_book.id,
            'title': new_book.title,
            'description': new_book.description,
            'price': new_book.price,
            'price_unit': new_book.price_unit,
            'pages': new_book.pages,
            'publication_date': new_book.publication_date,
            'isbn': new_book.isbn,
            'genre': new_book.genre,
            'user_id': new_book.user_id,
            'company_id': new_book.company_id,
        }

        # Building a response message
        return jsonify({"message": f"Book '{new_book.title}', ID '{new_book.id}' has been registered", "book": book_details}), 201

    except Exception as e:
        # Handle exceptions appropriately
        return jsonify({"error": str(e)}), 500
    
#get all books
@book.route('/books/', methods=['GET'])
def get_all_books():
    try:
        books = Book.query.all()
        output = []
        for book in books:
            book_data = {
                'title': book.title,
                'description':book.description,
                'price': book.price,
                'price_unit':book.price_unit,
                'pages':book.pages,
                'publication_date': book.publication_date,
                'isbn':book.isbn,
                'genre':book.genre,
                'user_id':book.user_id,
                'company_id': book.company_id
               
            }
            output.append(book_data)
        return jsonify({'books': output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get a specific book
@book.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        book = Book.query.get(id)
        if book:
            book_data = {
                'title': book.title,
                'description':book.description,
                'price': book.price,
                'price_unit':book.price_unit,
                'pages':book.pages,
                'publication_date': book.publication_date,
                'isbn':book.isbn,
                'genre':book.genre,
                'user_id':book.user_id,
                'company_id': book.company_id
            }
            return jsonify(book_data), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#update a book
@book.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    try:
        current_user_id = get_jwt_identity()
        book = Book.query.get(id)
        if book:
            data = request.json
            book.title = data.get('title', book.title)
            book.description = data.get('description', book.description)
            book.price = float(data.get('price', book.price))
            book.price_unit = data.get('price_unit', book.price_unit)
            book.pages = int(data.get('pages', book.pages))
            book.publication_date = data.get('publication_date', book.publication_date)
            book.isbn = data.get('isbn', book.isbn)
            book.genre = data.get('genre', book.genre)
            book.user_id = int(data.get('user_id', book.user_id))
            book.company_id = int(data.get('company_id', book.company_id))

            db.session.commit()
            return jsonify({"message": "Book created successfully"}), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#delete book
@book.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    try:
        current_user_id = get_jwt_identity()
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": "Book deleted successfully"}), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Cannot delete book due to associated records in the database"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
