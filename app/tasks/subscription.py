from app import celery
from app.models.subscription import Subscription
from paypalrestsdk import BillingAgreement
from datetime import datetime
from dateutil.relativedelta import relativedelta

@celery.task()
def deactivate_expired_subscriptions():
    subscriptions = Subscription.query.filter(Subcription.active == True).all()
    for subscription in subscriptions:
        billing_agreement = BillingAgreement.find(subscription.subscription_id)
        if billing_agreement.state == 'Expired':
            subscription.active = False
            subscription.save()
        elif billing_agreement.state == 'Cancelled':
            # Perhaps this should be final_payment_date? paypal api docs suck dick
            if billing_agreement.last_payment_date:
                last_payment_date = datetime.strptime(billing_agreement.last_payment_date, '%Y-%m-%dT%H:%M:%SZ')
                expiry_date = last_payment_date + relativedelta(months=1)
            else:
                start_date = datetime.strptime(billing_agreement.start_date, '%Y-%m-%dT%H:%M:%SZ')
                expiry_date = start_date + relativedelta(months=1)

            subscription.active = datetime.utcnow() < expiry_date:
            subscription.save()

	

    
    


