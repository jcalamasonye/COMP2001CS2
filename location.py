from flask import Blueprint, request, jsonify
from models import db, Location, location_schema, locations_schema
from sqlalchemy.exc import SQLAlchemyError

location_bp = Blueprint('location_bp', __name__)

# Get all locations
@location_bp.route('/locations', methods=['GET'])
def get_all_locations():
    try:
        locations = Location.query.all()
        if not locations:
            return jsonify({"message": "No locations found"}), 404
        return locations_schema.jsonify(locations)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Get a specific location by ID
@location_bp.route('/locations/<location_id>', methods=['GET'])
def get_location(location_id):
    try:
        location = Location.query.get_or_404(location_id)
        return location_schema.jsonify(location)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Create a new location
@location_bp.route('/locations', methods=['POST'])
def create_location():
    try:
        data = request.json
        # Validate required fields
        if not data.get('location_id') or not data.get('specific_location'):
            return jsonify({"error": "Missing required fields: location_id, specific_location"}), 400

        new_location = Location(**data)
        db.session.add(new_location)
        db.session.commit()
        return location_schema.jsonify(new_location), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing location
@location_bp.route('/locations/<location_id>', methods=['PUT'])
def update_location(location_id):
    try:
        location = Location.query.get_or_404(location_id)
        data = request.json

        # Ensure that the data is not empty
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        for key, value in data.items():
            setattr(location, key, value)

        db.session.commit()
        return location_schema.jsonify(location)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a specific location by ID
@location_bp.route('/locations/<location_id>', methods=['DELETE'])
def delete_location(location_id):
    try:
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return jsonify({"message": "Location deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
