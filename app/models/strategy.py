from .. import db

class Strategy(db.Model):
    __tablename__ = 'strategies'

    id = db.Column('strategy_id', db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String)
    quantopian_url = db.Column(db.String)
    price_history = db.relationship('PriceHistory', lazy=True)

    def __init__(self, name, description, quantopian_url):
        self.name = name
        self.description = description
        self.quantopian_url = quantopian_url


class PriceHistory(db.Model):
    __tablename__ = 'price_history'

    strategy_id = db.Column('strategy_id', db.Integer, db.ForeignKey('strategies.strategy_id'), primary_key=True)
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)


