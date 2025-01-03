from flask import Flask, jsonify, request, render_template

# Mock Database
mock_db = [
    {"fname": "John", "lname": "Doe"},
    {"fname": "Jane", "lname": "Smith"}
]

app = Flask(__name__)

# Home Route
@app.route("/")
def home():
    return render_template("home.html", people=mock_db)

# Swagger Routes
@app.route("/api/people", methods=["GET"])
def read_all():
    """Return all people from the mock database."""
    return jsonify(mock_db), 200

@app.route("/api/people", methods=["POST"])
def create():
    """Create a new person."""
    data = request.json
    if not data or "fname" not in data or "lname" not in data:
        return jsonify({"error": "Invalid input"}), 400

    mock_db.append(data)
    return jsonify(data), 201

@app.route("/api/people/<string:lname>", methods=["GET"])
def read_one(lname):
    """Return a single person by last name."""
    person = next((p for p in mock_db if p["lname"] == lname), None)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(person), 200

@app.route("/api/people/<string:lname>", methods=["PUT"])
def update(lname):
    """Update a person by last name."""
    data = request.json
    person = next((p for p in mock_db if p["lname"] == lname), None)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    if "fname" in data:
        person["fname"] = data["fname"]
    if "lname" in data:
        person["lname"] = data["lname"]

    return jsonify(person), 200

@app.route("/api/people/<string:lname>", methods=["DELETE"])
def delete(lname):
    """Delete a person by last name."""
    global mock_db
    person = next((p for p in mock_db if p["lname"] == lname), None)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    mock_db = [p for p in mock_db if p["lname"] != lname]
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
