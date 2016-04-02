import braintree
from paypalrestsdk import BillingAgreement

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

    payment_gateway = db.Column(db.String(128))

    plan_id = db.Column(db.String(128), db.ForeignKey('strategies.plan_id'))
    strategy = db.relationship('Strategy', lazy=True)

    # AKA Agreement Id for PayPal Gateways
    # TODO: Rename to gateway_subscription_id ?
    subscription_id = db.Column(db.String(128))

    active = db.Column(db.Boolean())

    def create(self, user=None, plan_id=None, subscription_id=None,
               payment_gateway=None):
	self.payment_gateway = payment_gateway
	self.user_id = user.id
	self.plan_id = plan_id
	self.subscription_id = subscription_id
	self.active = True

        db.session.add(self)
        db.session.commit()

	return True

    def create_braintree():
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

        #TODO: plan_id and user_id should be unique, I should be updating 
        # old plans if they get reactivated. Implement logic to check this in future.
        # otherwise you can end up with a bunch of unactive plans when you get the user.
        # Which may cause slowness for that user.

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
            self.active = True
        else:
            return result

        # Commit to database
        db.session.add(user)
        db.session.add(self)

        db.session.commit()

        return result

    def create_stripe():
        pass

    def create_paypal():
        pass
        

    def is_active(self):
        """ DEPERECIATED FUNCTION PLEASE USE active field of subscription"""
        return self.active

    def cancel(self):
    	if self.payment_gateway == 'paypal':
	    return self.cancel_paypal()

    def cancel_paypal(self):
	billing_agreement = BillingAgreement.find(self.subscription_id)    	
        cancel_note = {"note": "Canceled subscription."}
	if billing_agreement.cancel(cancel_note):
	    return True
	else:
	    return False
    	
    def cancel_braintree(self):
        result = braintree.Subscription.cancel(self.subscription_id)
        return result

