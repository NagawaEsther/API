from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required,get_jwt_identity,JWTManager
from authors_app.models.user import User
from authors_app import db
from authors_app.extensions import jwt



auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
bcrypt = Bcrypt()
jwt = JWTManager()

# Get all users
@auth.route('/users/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'contact': user.contact,
            'user_type': user.user_type,
            'biography': user.biography
        }
        output.append(user_data)
    return jsonify({'users': output})

# Get a specific user
@auth.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    user_data = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'contact': user.contact,
        'user_type': user.user_type,
        'biography': user.biography
    }
    return jsonify(user_data)

# Register a user
@auth.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Check if email or password is missing
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        # Validate email format
        validate_email(email)

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        new_user = User(
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            contact=data.get('contact'),
            user_type=data.get('user_type', 'author'),
            password=hashed_password,
            biography=data.get('biography', '')
        )

        db.session.add(new_user)
        db.session.commit()
        
        # Return user details in response
        user_details = {
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'contact': new_user.contact,
            'user_type': new_user.user_type,
            'biography': new_user.biography
        }

        return jsonify({'message': 'User registered successfully', 'user': user_details}), 201

    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a user
@auth.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get_or_404(id)
        data = request.get_json()
        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.contact = data.get('contact', user.contact)
        user.user_type = data.get('user_type', user.user_type)
        password = data.get('password')
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.biography = data.get('biography', user.biography)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a user
@auth.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500
    
# Authentication endpoint to handle user login
@auth.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # A dictionary containing user details
        user_info = {
            'id': user.id,
            'email': user.email,
            'name':user.last_name
        }

        access_token = create_access_token(identity=user_info)

        # Including user details in the response
        return jsonify({
            'access_token': access_token,
            'user': user_info
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
