from app import db
from app.utils.sqlalchemy_util import ResourceMixin

class Strategy(ResourceMixin, db.Model):
    __tablename__ = 'strategies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String)
    quantopian_url = db.Column(db.String)
    returns = db.relationship('Returns', lazy=True)

class Returns(db.Model):
    __tablename__ = 'returns'

    strategy_id = db.Column('strategy_id',
                            db.Integer,
                            db.ForeignKey('strategies.id'),
                            primary_key=True)
    date = db.Column(db.DateTime)

    # Can't use 'return' maybe I should change this
    # it seems dangerous. But I'm too ocd on naming variables.
    return_ = db.Column('return', db.Float)


