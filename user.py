from flask import Blueprint, request, jsonify
from models import db, User, user_schema, users_schema
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({"message": "No users found"}), 404
        return users_schema.jsonify(users)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Get a specific user by ID
@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# # Create a new user
# @user_bp.route('/users', methods=['POST'])
# def create_user():
#     try:
#         data = request.json
#         print(data)

#         # Validate required fields
#         # if not data.get('username') or not data.get('email'):
#         #     return jsonify({"error": "Missing required fields: username, email"}), 400

#         new_user = User(**data)
#         db.session.add(new_user)
#         db.session.commit()
#         return user_schema.jsonify(new_user), 201
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json

        # Validate required fields
        if not data.get('user_name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields: user_name, email, password"}), 400

        # Hash the password
        hashed_password = generate_password_hash(data['password'])

        # Create a new user instance
        new_user = User(
            user_id=data.get('user_id', '').upper(),
            user_name=data['user_name'].title(),
            email=data['email'],
            phone_number=data.get('phone_number'),
            password=hashed_password
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# User login
@user_bp.route('/users/login', methods=['POST'])
def login_user():
    try:
        data = request.json

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields: email, password"}), 400

        # Find the user by email
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Check the password
        if not check_password_hash(user.password, data['password']):
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({"message": "Login successful", "user_id": user.user_id}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update an existing user
@user_bp.route('/users/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    print("user_id",user_id)
    try:
        user = User.query.get_or_404(user_id)
        data = request.json

        # Ensure that the data is not empty
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()
        return user_schema.jsonify(user)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a specific user by ID
@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        print(user_id)
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
