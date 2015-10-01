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

@billing.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    plan_id = request.args.get('plan_id')
    form = PaymentForm(plan_id=plan_id)
    if form.validate_on_submit():
        plan_id = request.form.get('plan_id')
        nonce = request.form.get("payment_method_nonce")

        # Create Subscription
        subscription = Subscription()
        created = subscription.create(current_user, plan_id, nonce)
        if created.is_success:
            return redirect(url_for('billing.confirmation'))

    token = braintree.ClientToken.generate()
    return render_template('billing/subscribe.html', form=form, token=token)

@billing.route('/confirmation')
def confirmation():
    return render_template('billing/confirmation.html')


