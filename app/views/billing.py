from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import current_user, login_required
import braintree

from app.forms.billing import PaymentForm
from app.models.subscription import Subscription

billing = Blueprint('billing', __name__, url_prefix='/billing')

# TODO: Path should be /subscribe/<strategy_name> or the plan_id 
@billing.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    # THIS FUNCTION SUBSCRIBES TO THE SAME STRATEGY. CHANGE
    # WHEN YOU HAVE MULTIPLE STRATEGIES
    # TODO: Put plan_id as a constant since I use it in multiple places
    plan_id = 'standard-plan'

    # Don't allow user to resubscribe if they already subscribed.
    if current_user.is_subscribed(plan_id):
        #flash("You area already subscribed to this strategy")
        return redirect(url_for('strategy.strategy_details',
                        strategy_name=plan_id))

    form = PaymentForm(plan_id=plan_id)
    if form.validate_on_submit():
        #plan_id = request.form.get('plan_id')
        nonce = request.form.get("payment_method_nonce")

        # Create Subscription
        subscription = Subscription()
        created = subscription.create(current_user, plan_id, nonce)
        if created.is_success:
            return redirect(url_for('billing.confirmation', plan_id=plan_id))
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

    token = braintree.ClientToken.generate()
    return render_template('billing/subscribe.html', form=form, token=token)

@billing.route('/confirmation')
def confirmation():
    plan_id = request.args.get('plan_id')
    return render_template('billing/confirmation.html', plan_id=plan_id)

@billing.route('/cancel', methods=['GET', 'POST'])
def cancel():
    pass

