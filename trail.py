from flask import Blueprint, request, jsonify
from models import db, Trail, trail_schema, trails_schema
from sqlalchemy.exc import SQLAlchemyError

trail_bp = Blueprint('trail_bp', __name__)

# Get all trails
@trail_bp.route('/trails', methods=['GET'])
def get_all_trails():
    try:
        trails = Trail.query.all()
        if not trails:
            return jsonify({"message": "No trails found"}), 404
        return trails_schema.jsonify(trails)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Get a specific trail by ID
@trail_bp.route('/trails/<trail_id>', methods=['GET'])
def get_trail(trail_id):
    try:
        trail = Trail.query.get_or_404(trail_id)
        return trail_schema.jsonify(trail)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Create a new trail
@trail_bp.route('/trails', methods=['POST'])
def create_trail():
    try:
        data = request.json
        # Validate required fields
        if not data.get('trail_id') or not data.get('trail_name') or not data.get('location_id'):
            return jsonify({"error": "Missing required fields: trail_id, trail_name, location_id"}), 400

        new_trail = Trail(**data)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.jsonify(new_trail), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing trail
@trail_bp.route('/trails/<trail_id>', methods=['PUT'])
def update_trail(trail_id):
    try:
        trail = Trail.query.get_or_404(trail_id)
        data = request.json

        # Ensure that the data is not empty
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        for key, value in data.items():
            setattr(trail, key, value)

        db.session.commit()
        return trail_schema.jsonify(trail)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a specific trail by ID
@trail_bp.route('/trails/<trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    try:
        trail = Trail.query.get_or_404(trail_id)
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
