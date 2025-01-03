import pytz
from datetime import datetime
from config import db, ma


class TrailView(db.Model):
    __tablename__ = "trail_view"

    view_id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
    trail_id = db.Column(db.String(10), db.ForeignKey("trail.trail_id"), nullable=False)
    user_id = db.Column(db.String(8), db.ForeignKey("user.user_id"), nullable=True)
    view_type = db.Column(db.String(50), nullable=True)
    terrain_type = db.Column(db.String(30), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    def __init__(self, **kwargs):
        # Validation for converting inputs to required format
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
