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
def subscribe():
    plan_id = request.args.get('plan_id')

    # Don't allow user to resubscribe if they already subscribed.
    plans = filter(lambda subscription: subscription.plan_id == plan_id,
                  current_user.subscriptions)
    if len(plans) and plans[-1].is_active():
        return redirect(url_for('strategy.strategy_details',
                        strategy_name=plan_id))

    form = PaymentForm(plan_id=plan_id)
    if form.validate_on_submit():
        plan_id = request.form.get('plan_id')
        nonce = request.form.get("payment_method_nonce")

        # Create Subscription
        subscription = Subscription()
        created = subscription.create(current_user, plan_id, nonce)
        if created.is_success:
            return redirect(url_for('billing.confirmation', plan_id=plan_id))

    token = braintree.ClientToken.generate()
    return render_template('billing/subscribe.html', form=form, token=token)

@billing.route('/confirmation')
def confirmation():
    plan_id = request.args.get('plan_id')
    return render_template('billing/confirmation.html', plan_id=plan_id)

@billing.route('/cancel', methods=['GET', 'POST'])
def cancel():
    pass

