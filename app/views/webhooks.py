from flask import Blueprint, request, render_template, Response
from app.models.subscription import Subscription
import braintree

webhooks = Blueprint('webhooks', __name__)

@webhooks.route('/braintree_webhook/event', methods=['POST'])
def braintree_event():
    bt_signature_param = request.form['bt_signature']
    bt_payload_param = request.form['bt_payload']
    webhook_notification = braintree.WebhookNotification.parse(
        bt_signature_param, bt_payload_param
    )

    subscription_id = webhook_notification.subscription.id
    subscription = Subscription.query.filter_by(subscription_id=subscription_id).first()

    if webhook_notification.kind == braintree.WebhookNotification.Kind.SubscriptionChargedSuccessfully:
        subscription.active = True
    elif webhook_notification.kind == braintree.WebhookNotification.Kind.SubscriptionCanceled:
        subscription.active = False

    return Response(status=200)
