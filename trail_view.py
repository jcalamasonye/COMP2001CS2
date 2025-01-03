from flask import Blueprint, request, jsonify
# from models import db, TrailView, trail_view_schema, trail_views_schema
from models import db, TrailView, trail_view_schema, trail_views_schema, User,Trail
from sqlalchemy.exc import SQLAlchemyError

trail_view_bp = Blueprint('trail_view_bp', __name__)

# Get all trail views
@trail_view_bp.route('/trail_views', methods=['GET'])
def get_all_trail_views():
    try:
        trail_views = TrailView.query.all()
        if not trail_views:
            return jsonify({"message": "No trail views found"}), 404
        return trail_views_schema.jsonify(trail_views)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Get a specific trail view by ID
@trail_view_bp.route('/trail_views/<view_id>', methods=['GET'])
def get_trail_view(view_id):
    try:
        trail_view = TrailView.query.get_or_404(view_id)
        return trail_view_schema.jsonify(trail_view)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


# Create a new trail view
@trail_view_bp.route('/trail_views', methods=['POST'])
def create_trail_view():
    try:
        data = request.json
        # Validate required fields
        if not data.get('view_id') or not data.get('trail_id') or not data.get('user_id'):
            return jsonify({"error": "Missing required fields: view_id, trail_id, user_id"}), 400
        
        # Check if the user exists
        user = User.query.get(data.get('user_id'))
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if the trail exists
        trail = Trail.query.get(data.get('trail_id'))
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        # Proceed to create the trail view if both user and trail exist
        new_trail_view = TrailView(**data)
        db.session.add(new_trail_view)
        db.session.commit()

        return trail_view_schema.jsonify(new_trail_view), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Update an existing trail view
@trail_view_bp.route('/trail_views/<view_id>', methods=['PUT'])
def update_trail_view(view_id):
    try:
        trail_view = TrailView.query.get_or_404(view_id)
        data = request.json

        # Ensure that the data is not empty
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        for key, value in data.items():
            setattr(trail_view, key, value)

        db.session.commit()
        return trail_view_schema.jsonify(trail_view)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a specific trail view by ID
@trail_view_bp.route('/trail_views/<view_id>', methods=['DELETE'])
def delete_trail_view(view_id):
    try:
        trail_view = TrailView.query.get_or_404(view_id)
        db.session.delete(trail_view)
        db.session.commit()
        return jsonify({"message": "Trail View deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
