
import pytz
from datetime import datetime
from config import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.security import generate_password_hash, check_password_hash


# Location Model
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


# TrailView Model
class TrailView(db.Model):
    __tablename__ = "trail_view"

    view_id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
    trail_id = db.Column(db.String(10), db.ForeignKey("trail.trail_id"), nullable=False, unique=True)
    user_id = db.Column(db.String(8), db.ForeignKey("user.user_id"), nullable=True)
    view_type = db.Column(db.String(50), nullable=True)
    terrain_type = db.Column(db.String(30), nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/London")),
        onupdate=lambda: datetime.now(pytz.timezone("Europe/London")),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.view_id:
            self.view_id = self.view_id.upper()
        if self.trail_id:
            self.trail_id = self.trail_id.upper()
        if self.user_id:
            self.user_id = self.user_id.upper()
        if self.view_type:
            self.view_type = self.view_type.title()
        if self.terrain_type:
            self.terrain_type = self.terrain_type.title()



class TrailViewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailView
        load_instance = True
        sqla_session = db.session


trail_view_schema = TrailViewSchema()
trail_views_schema = TrailViewSchema(many=True)


# Trail Model
class Trail(db.Model):
    __tablename__ = "trail"

    trail_id = db.Column(db.String(10), primary_key=True)  # Ensure trail_id is a primary key
    trail_name = db.Column(db.String(255), nullable=False)
    location_id = db.Column(db.String(8), db.ForeignKey('location.location_id'), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(5), nullable=True)  # Format HH:MM
    elevation_gain = db.Column(db.Float, nullable=True)
    route_type = db.Column(db.String(20), nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/London")),
        onupdate=lambda: datetime.now(pytz.timezone("Europe/London")),
    )

    # Relationships
    location = db.relationship("Location", backref="trails", lazy=True)

    # Relationship to TrailView (one-to-one)
    trail_view = db.relationship("TrailView", backref="trail", uselist=False)

    def __init__(self, **kwargs):
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



class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session


trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)




# TrailLog Model
class TrailLog(db.Model):
    __tablename__ = "trail_log"

    # Columns
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_id = db.Column(db.String(10), db.ForeignKey("trail.trail_id"), nullable=False)  # Foreign key reference to Trail
    added_by = db.Column(db.String(100), nullable=False)
    time_added = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London'))  # Default to current time in Europe/London timezone
    )

    # Relationship to Trail
    trail = db.relationship("Trail", backref="trail_logs", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.added_by:
            self.added_by = self.added_by.title()


# TrailLog Schema
class TrailLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailLog
        load_instance = True
        sqla_session = db.session


# Single and multiple TrailLog schemas
trail_log_schema = TrailLogSchema()
trail_logs_schema = TrailLogSchema(many=True)



# # User Model
# class User(db.Model):
#     __tablename__ = "user"

#     user_id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
#     user_name = db.Column(db.String(225), nullable=True)
#     email = db.Column(db.String(225), nullable=False)
#     phone_number = db.Column(db.BigInteger, nullable=True)
#     timestamp = db.Column(
#         db.DateTime,
#         default=lambda: datetime.now(pytz.timezone('Europe/London')),
#         onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
#     )

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         if self.user_id:
#             self.user_id = self.user_id.upper()
#         if self.user_name:
#             self.user_name = self.user_name.title()


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         load_instance = True
#         sqla_session = db.session


# user_schema = UserSchema()
# users_schema = UserSchema(many=True)



# User Model
class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
    user_name = db.Column(db.String(225), nullable=True)
    email = db.Column(db.String(225), nullable=False, unique=True)
    phone_number = db.Column(db.BigInteger, nullable=True)
    password = db.Column(db.String(128), nullable=False)  # Store hashed passwords
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.user_id:
            self.user_id = self.user_id.upper()
        if self.user_name:
            self.user_name = self.user_name.title()
        # if 'password' in kwargs:
        #     self.set_password(kwargs['password'])  # Hash the password during initialization

    # def set_password(self, password):
    #     """Hashes and sets the user's password."""
    #     self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     """Verifies the password against the stored hash."""
    #     return check_password_hash(self.password, password)


# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    password = ma.auto_field(load_only=True)  # Allow password input but do not serialize it


# Single and multiple User schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)


