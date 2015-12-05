from app import db
from app.utils.sqlalchemy_util import ResourceMixin

class Security(ResourceMixin, db.Model):
    __tablename__ = 'securities'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(128))
    name = db.Column(db.String(128))
