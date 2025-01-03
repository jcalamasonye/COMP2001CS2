from flask import Blueprint, request, jsonify
from models import db, TrailLog, trail_log_schema, trail_logs_schema
from sqlalchemy.exc import SQLAlchemyError

# Create the blueprint
trail_log_bp = Blueprint('trail_log_bp', __name__)

# Get all trail logs
@trail_log_bp.route('/trail_logs', methods=['GET'])
def get_all_trail_logs():
    try:
        trail_logs = TrailLog.query.all()
        if not trail_logs:
            return jsonify({"message": "No trail logs found"}), 404
        return trail_logs_schema.jsonify(trail_logs), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Get a specific trail log by ID
@trail_log_bp.route('/trail_logs/by_id/<int:log_id>', methods=['GET'])
def get_trail_log(log_id):
    try:
        trail_log = TrailLog.query.get_or_404(log_id)
        return trail_log_schema.jsonify(trail_log), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Create a new trail log
@trail_log_bp.route('/trail_logs', methods=['POST'])
def create_trail_log():
    try:
        data = request.json

        # Validate required fields
        if not data.get('trail_id') or not data.get('added_by'):
            return jsonify({"error": "Missing required fields: trail_id, added_by"}), 400

        new_trail_log = TrailLog(
            trail_id=data['trail_id'],
            added_by=data['added_by']
        )

        db.session.add(new_trail_log)
        db.session.commit()
        return trail_log_schema.jsonify(new_trail_log), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing trail log
@trail_log_bp.route('/trail_logs/<int:log_id>', methods=['PUT'])
def update_trail_log(log_id):
    try:
        trail_log = TrailLog.query.get_or_404(log_id)
        data = request.json

        # Ensure that the data is not empty
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        for key, value in data.items():
            setattr(trail_log, key, value)

        db.session.commit()
        return trail_log_schema.jsonify(trail_log), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a specific trail log by ID
@trail_log_bp.route('/trail_logs/<int:log_id>', methods=['DELETE'])
def delete_trail_log(log_id):
    try:
        trail_log = TrailLog.query.get_or_404(log_id)
        db.session.delete(trail_log)
        db.session.commit()
        return jsonify({"message": "Trail Log deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
