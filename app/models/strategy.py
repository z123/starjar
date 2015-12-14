from app import db
from app.utils.sqlalchemy_util import ResourceMixin

strategy_security_link = db.Table('strategy_security_link',
    db.Column('strategy_id', db.Integer, db.ForeignKey('strategies.id')),
    db.Column('security_id', db.Integer, db.ForeignKey('securities.id')),
)

class Strategy(ResourceMixin, db.Model):
    __tablename__ = 'strategies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String)
    quantopian_url = db.Column(db.String)
    returns = db.relationship('Return', backref='strategy', lazy=True)
    positions = db.relationship('Security', lazy=True, secondary='strategy_security_link')

    # Billing
    plan_id = db.Column(db.String(128))

# Using 'Return' seems dangerous. But I'm too ocd on naming.
class Return(db.Model):
    __tablename__ = 'returns'

    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column('strategy_id',
                            db.Integer,
                            db.ForeignKey('strategies.id'))
    date = db.Column(db.DateTime)

    gain = db.Column('gain', db.Float)


