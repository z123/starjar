from app import db
from app.utils.sqlalchemy_util import ResourceMixin

class StrategyStockLink(db.Tabel):
    __tablename__ = 'strategy_stock_link'
    db.Column('strategy_id', db.Integer, db.ForeignKey('strategy.id')),
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.id')),

class Strategy(ResourceMixin, db.Model):
    __tablename__ = 'strategies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String)
    quantopian_url = db.Column(db.String)
    returns = db.relationship('Returns', backref='strategy', lazy=True)
    positions = db.relationship('Stock', lazy=True, secondary='StrategyStockLink')

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


