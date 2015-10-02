import braintree

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
    payment_method_token = db.Column(db.String(128))

    def create(self, user=None, plan_id=None, payment_method_nonce=None):
        """
        Create a recurring subscription.
        :param user: User to apply the subscription to
        :type user: User instance
        :param name: User's billing name
        :type name: str
        :param plan: Plan identifier
        :type plan: str
        :param coupon: Coupon code to apply
        :type coupon: str
        :param token: Token returned by javascript
        :type token: str
        :return: bool
        """

        # Set the subscription details.
        self.user_id = user.id
        self.plan_id = plan_id

        # Create the user account if none exists.
        if user.customer_id is None:
            result = braintree.Customer.create()
            if result.is_success:
                user.customer_id = result.customer.id
            else:
                return result

        # Create the payment method
        result = braintree.PaymentMethod.create({
            'customer_id': user.customer_id,
            'payment_method_nonce': payment_method_nonce,
            'options': {
                'verify_card': True
            }
        })

        if result.is_success:
            self.payment_method_token = result.payment_method.token
        else:
            return result

        # Create subscription
        result = braintree.Subscription.create({
            'payment_method_token': self.payment_method_token,
            'plan_id': plan_id
        })

        if result.is_success:
            self.subscription_id = result.subscription.id
        else:
            return result

        # Commit to database
        db.session.add(user)
        db.session.add(self)

        db.session.commit()

        return result

    def is_active(self):
        # TODO: Better to use webhooks rather than querying braintree
        # everytime. Implement sometime in the future.
        subscription = braintree.Subscription.find(self.subscription_id)
        return subscription == braintree.Subscription.status.Active

