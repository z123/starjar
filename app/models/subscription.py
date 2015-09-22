from app import db
from app.utils.sqlalchemy_util import ResourceMixin

class Subscription(ResourceMixin, db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)

    # Braintree details
    plan_id = db.Column(db.String(128))
    subscription_id = db.Column(db.String(128))


