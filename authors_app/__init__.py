from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory
import os  

# Initialize SQLAlchemy db object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize JWTManager with secret key
    app.config['JWT_SECRET_KEY'] = '12345'  # secret key
    jwt = JWTManager(app)

    # Import blueprints
    from authors_app.controllers.auth.auth_controller import auth
    from authors_app.controllers.auth.books_controller import book
    from authors_app.controllers.auth.company_controller import company
    
    
    # Register blueprints
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(book, url_prefix='/api/v1/book')
    app.register_blueprint(company, url_prefix='/api/v1/company')
    
    # Serve Swagger JSON file
    @app.route('/swagger.json')
    def serve_swagger_json():
        try:
            return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

        except FileNotFoundError:
            return jsonify({"message": "Swagger JSON file not found"}), 404
    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/swagger.json'  # URL to your Swagger JSON file 
    
    # Create Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "authorsapi_app"
        }
    )
    
    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint)

    @app.route('/')
    def home():
        return "Hello world"

    # Routes for protected resources
    @app.route('/protected')
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
