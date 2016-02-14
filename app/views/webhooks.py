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

    if webhook_notification.kind == braintree.WebhookNotification.Kind.SubscriptionWentActive:
        subscription.active = True
    elif webhook_notification.kind == braintree.WebhookNotification.Kind.SubscriptionExpired:
        subscription.active = False
    subscription.save()

    return Response(status=200)
