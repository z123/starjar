from app import db
from app.utils.sqlalchemy_util import ResourceMixin

class Strategy(ResourceMixin, db.Model):
    __tablename__ = 'strategies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String)
    quantopian_url = db.Column(db.String)

    # Billing
    # plan ids should always be lower cased dashed version of name
    plan_id = db.Column(db.String(128), unique=True)
