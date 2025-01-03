import pytz
from datetime import datetime
from config import db, ma


class Location(db.Model):
    __tablename__ = "location"

    location_id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
    specific_location = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    county = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    def __init__(self, **kwargs):
        # Validation for converting inputs to required format
        super().__init__(**kwargs)
        if self.location_id:
            self.location_id = self.location_id.upper()
        if self.specific_location:
            self.specific_location = self.specific_location.title()
        if self.city:
            self.city = self.city.title()
        if self.county:
            self.county = self.county.title()
        if self.country:
            self.country = self.country.title()


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
