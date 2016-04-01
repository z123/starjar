from app import db
from app.models.strategy import Strategy
from app.models.user import User
from paypalrestsdk import BillingPlan, ResourceNotFound
from app import app
from flask import url_for

def create_admin():
    params = {
        'role': 'admin',
        'email': 'support@equitybuilder.io',
        'password': 'bibirkobr'
    }

    return User(**params).save()

def create_strategies():

    params = {
        'name': "Standard Strategy",
        'description': "",
        'quantopian_url': "https://www.quantopian.com/algorithms/56d884653e72f1938700082d",
        'plan_id': create_plan().id
    }

    return Strategy(**params).save()

# def delete_plan():
    # all_plans = BillingPlan.all()
    # for plan in all_plans.plans:
	# BillingPlan.find(plan.id) \
	# .replace([{"op": "replace","path": "/","value": {"state":"DELETED"}}])

def create_plan():
    with app.app_context():
	billing_plan = BillingPlan({
	    "name": "EquityBuilder Subscription",
            "description": "$10 monthly subscription to EquityBuilder.",
	    "payment_definitions": [
		{
		    "name": "Standard Plan",
		    "type": "REGULAR",
		    "frequency_interval": "1",
		    "frequency": "MONTH",
		    "cycles": "0",
		    "amount": {
			"currency": "USD",
			"value": "10"
		    }
		}
	    ],
	    "merchant_preferences": {
		"auto_bill_amount": "YES",
		"cancel_url": url_for('billing.subscribe'),
		"initial_fail_amount_action": "CANCEL",
		"max_fail_attempts": "1",
		"return_url": url_for('billing.subscribe_paypal'),
		"setup_fee": {
		    "currency": "USD",
		    "value": "10"
		}
	    },
	    "type": "INFINITE"
	})

	if billing_plan.create() and billing_plan.activate():
	    return billing_plan
	else:
            return billing_plan.error


def seed():
    """Seeds database with dummy data."""
    create_admin()
    create_strategies()

def reset():
    db.drop_all()
    db.create_all()
    seed()


