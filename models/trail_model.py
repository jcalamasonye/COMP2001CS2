import pytz
from datetime import datetime
from config import db, ma


class Trail(db.Model):
    __tablename__ = "trail"

    trail_id = db.Column(db.String(10), primary_key=True, unique=True, nullable=False)
    trail_name = db.Column(db.String(50), nullable=False)
    location_id = db.Column(db.String(10), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    distance = db.Column(db.Float, nullable=True)  # Distance in kilometers
    duration = db.Column(db.String(5), nullable=True)  # Format HH:MM
    elevation_gain = db.Column(db.Float, nullable=True)  # Elevation in meters
    route_type = db.Column(db.String(20), nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    def __init__(self, **kwargs):
        # Validation for converting inputs to required format
        super().__init__(**kwargs)
        if self.trail_id:
            self.trail_id = self.trail_id.upper()
        if self.location_id:
            self.location_id = self.location_id.upper()
        if self.trail_name:
            self.trail_name = self.trail_name.title()
        if self.difficulty:
            allowed_difficulties = {"Easy", "Moderate", "Hard"}
            if self.difficulty not in allowed_difficulties:
                raise ValueError(f"Difficulty must be one of {allowed_difficulties}")

    # Additional methods (if needed) for validation can be added here


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session


trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
