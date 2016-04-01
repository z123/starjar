from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import current_user, login_required
import braintree
from paypalrestsdk import BillingAgreement
import datetime
import calendar
from dateutil.relativedelta import relativedelta

from app.forms.billing import PaymentForm
from app.models.subscription import Subscription
from app.utils import datetime_util
from app.utils.constants import STANDARD_PLAN_ID

billing = Blueprint('billing', __name__, url_prefix='/billing')

# TODO: Path should be /subscribe/<strategy_name> or the plan_id 
@billing.route('/subscribe/paypal', methods=['GET'])
@login_required
def subscribe_paypal():
    token = request.args.get('token')
    if token:
	billing_agreement = BillingAgreement.execute(token)
	if billing_agreement:
	    subscription = Subscription()
	    subscription.create(current_user, STANDARD_PLAN_ID, billing_agreement.id, 'paypal')
	    flash("Thank you for subscribing.")
            return redirect(url_for('user.subscription'))
    else:
	start_date = datetime.datetime.utcnow() + relativedelta(months=1)
	billing_agreement = BillingAgreement({
	    "name": "EquityBuilder Subscription",
            "description": "Price: $10/month",
	    "start_date": start_date.strftime("%Y-%m-%dT00:00:00Z"),
	    "plan": {
		"id": STANDARD_PLAN_ID
	    },
	    "payer": {
		"payment_method": "paypal"
	    }
	})
	if billing_agreement.create():
	    for link in billing_agreement.links:
		if link.rel == "approval_url":
		    approval_url = link.href
		    return redirect(approval_url)
    flash("Something went wrong. Please try again.")
    return redirect(url_for('billing.subscribe'))
    
@billing.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    # Don't allow user to resubscribe if they already subscribed.
    if current_user.is_subscribed(STANDARD_PLAN_ID):
        #flash("You area already subscribed to this strategy")
        return redirect(url_for('user.subscription'))

    form = PaymentForm()
    if form.validate_on_submit():
        nonce = request.form.get("payment_method_nonce")

        # Create Subscription
        subscription = Subscription()
        created = subscription.create(current_user, plan_id, nonce)
        if created.is_success:
            flash("Thank you for subscribing.")
            return redirect(url_for('user.subscription'))
        else:
            errors = created.errors.deep_errors
            # Filters out wierd errors, look up errors if curious
            # TODO: Create a function that parses braintree errors
            # and returns nice and cleanly messaged errors
            errors = filter(lambda error: error.attribute != 'base', errors)
            errors = filter(lambda error: error.code != '81703', errors)

            if len(errors):
                flash(errors[0].message)
            else:
                flash('Invalid credit card')
    elif len(form.errors):
            flash(form.errors.values()[0][0], 'error')

    return render_template('billing/subscribe.html', form=form)

@billing.route('/confirm')
def confirm():
    return

@billing.route('/confirmation')
def confirmation():
    plan_id = request.args.get('plan_id')
    return render_template('billing/confirmation.html', plan_id=plan_id)

@billing.route('/cancel', methods=['GET', 'POST'])
def cancel():
    pass
