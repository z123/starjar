from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import current_user, login_required

billing = Blueprint('billing', __name__)

@billing.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    plan_id = request.args.get('plan_id')
    return current_user.email
