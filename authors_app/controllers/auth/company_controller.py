from flask import Blueprint, request, jsonify
from authors_app.models.company import Company, db
from authors_app.models.user import User
from flask_jwt_extended import jwt_required,get_jwt_identity

company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
@jwt_required()
def register_company():
    try:
        # Extracting request data
        #company_id = request.json.get('company_id')
        name = request.json.get('name')
        origin = request.json.get('origin')
        description = request.json.get('description')
        #user_id = request.json.get('user_id')  

        # Getting current user ID from JWT token
        current_user_id=get_jwt_identity()
        print("Token identity:",current_user_id)

        #Extract user ID from token identity
        current_user_id = current_user_id['id']

        # Basic input validation
        #if not company_id:
            #return jsonify({"error": 'Company ID is required'}), 400

        if not name:
            return jsonify({"error": 'Company name is required'}), 400

        if not origin:
            return jsonify({"error": 'Company origin is required'}), 400

        if not description:
            return jsonify({"error": 'Company description is required'}), 400
        
        if Company.query.filter_by(name=name).first():
            return jsonify({"error":"company name already exists"}),400


        # Check if the user exists
        user = User.query.get(current_user_id)
        
        #Debugging: Print user retrieved from database
        print("User retrieved from database:", user)
        
        # if user is None:
        #     return jsonify({"error": 'User with the provided ID does not exist'}), 404

        # Creating a new company
        new_company = Company(
            #id=company_id,
            name=name,
            origin=origin,
            description=description,
            user_id=current_user_id
        )

        db.session.add(new_company)
        db.session.commit()

        # Return company details in response
        company_details = {
            'id': new_company.id,
            'name': new_company.name,
            'origin': new_company.origin,
            'description': new_company.description,
            'user_id': new_company.user_id,
        }
        # Building a response message
        message = f"Company '{new_company.name}' with ID '{new_company.id}' has been registered"
        return jsonify({"message": message, "company": company_details}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


#get all companies
@company.route('/companies/', methods=['GET'])
def get_all_companies():
    try:
        companies = Company.query.all()
        output = []
        for company in companies:
            company_data = {
                'id': company.id,
                'name': company.name,
                'origin': company.origin,
                'description': company.description,
                'user_id': company.user_id
            }
            output.append(company_data)
        return jsonify({'companies': output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#get a specific company
@company.route('/companies/<int:id>', methods=['GET'])
def get_company(id):
    try:
        company = Company.query.get(id)
        if company:
            company_data = {
                'id': company.id,
                'name': company.name,
                'origin': company.origin,
                'description': company.description,
                'user_id': company.user_id
            }
            return jsonify(company_data), 200
        else:
            return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#Delete a company
@company.route('/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if the user has permissions to delete the company
        company = Company.query.get(id)
        if company:
            db.session.delete(company)
            db.session.commit()
            return jsonify({"message": "Company deleted successfully"}), 200
        else:
            return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
#update a company
@company.route('/companies/<int:id>', methods=['PUT'])
@jwt_required()
def update_company(id):
    try:
        company = Company.query.get(id)
        if company:
            data = request.json
            company.name = data.get('name', company.name)
            company.origin = data.get('origin', company.origin)
            company.description = data.get('description', company.description)
            company.user_id =data.get('user_id',company.user_id)
            db.session.commit()
            return jsonify({"message": "Company updated successfully"}), 200
        else:
            return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
