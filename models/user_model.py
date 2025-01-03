import pytz
from datetime import datetime
from config import db, ma


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
    user_name = db.Column(db.String(225), nullable=True)
    email = db.Column(db.String(225), nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    def __init__(self, **kwargs):
        # Validation for converting inputs to required format
        super().__init__(**kwargs)
        if self.user_id:
            self.user_id = self.user_id.upper()
        if self.user_name:
            self.user_name = self.user_name.title()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


user_schema = UserSchema()
users_schema = UserSchema(many=True)
