from collections import OrderedDict

from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

from app import bcrypt, db
from app.models.subscription import Subscription
from app.utils.sqlalchemy_util import ResourceMixin

class User(UserMixin, ResourceMixin, db.Model):
    ROLE = OrderedDict([
        ('guest', 'Guest'),
        ('member', 'Member'),
        ('admin', 'Admin')
    ])

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(128))
    role = db.Column(db.Enum(*ROLE, name='role_types'),
                     nullable=False, server_default='member')

    # Relationships
    subscriptions = db.relationship(Subscription, backref='users', passive_deletes=True)

    # Billing
    customer_id = db.Column(db.String(128))


    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def is_subscribed(self, plan_id):
        plans = filter(lambda subscription: subscription.plan_id == plan_id,
                      self.subscriptions)
        subscribed = len(plans) and plans[-1].is_active()

        return subscribed


