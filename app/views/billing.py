from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import current_user, login_required
import braintree

billing = Blueprint('billing', __name__, prefix='/billing')

@billing.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    plan_id = request.args.get('plan_id')
    token = braintree.ClientToken.generate()
    return render_template('billing/subscribe.html', token=token)
