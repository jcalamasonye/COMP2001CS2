from flask import render_template
import config

from config import db, ma

# Import blueprints
from trail import trail_bp
from location import location_bp
from trail_view import trail_view_bp
from user import user_bp
from trail_logs import trail_log_bp

# Get the app object from config
app = config.connex_app

# Register the blueprints using app.app (accessing the underlying Flask instance)
app.app.register_blueprint(trail_bp, url_prefix='/trails')
app.app.register_blueprint(location_bp, url_prefix='/locations')
app.app.register_blueprint(trail_view_bp, url_prefix='/trail-views')
app.app.register_blueprint(user_bp, url_prefix='/users')
app.app.register_blueprint(trail_log_bp, url_prefix='/trail_logs')

# Add API routes (if using Flask-Connexion)
app.add_api(config.basedir / "swagger.yml")

@app.route("/hello")
def home():
    return "welcome"

# Create all tables within the application context
with app.app.app_context():  # Use app.app to get the underlying Flask app
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

