from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')

app.config.from_pyfile('config.py', silent=True)

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()

# import braintree

# braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  # merchant_id=app.config.get('BT_MERCHANT_ID'),
                                  # public_key=app.config.get('BT_PUBLIC_KEY'),
                                  # private_key=app.config.get('BT_PRIVATE_KEY'))

import paypalrestsdk
paypalrestsdk.configure({
    'mode': app.config.get('PAYPAL_MODE'),
    'client_id': app.config.get('PAYPAL_CLIENT_ID'),
    'client_secret': app.config.get('PAYPAL_CLIENT_SECRET')
})

import paypal 
paypal = paypal.PayPalInterface(API_ENVIRONMENT=app.config.get('PAYPAL_API_ENVIRONMENT'),
                         API_USERNAME=app.config.get('PAYPAL_API_USERNAME'),
                         API_PASSWORD=app.config.get('PAYPAL_API_PASSWORD'),
                         API_SIGNATURE=app.config.get('PAYPAL_API_SIGNATURE'))

from flask_mail import Mail
mail = Mail(app)

# Views
from app.views.page import page
from app.views.strategy import strategy
from app.views.user import user
from app.views.billing import billing
from app.views.webhooks import webhooks

app.register_blueprint(page)
app.register_blueprint(strategy)
app.register_blueprint(user)
app.register_blueprint(billing)
app.register_blueprint(webhooks)

# Models
# TODO: Delete models not used 
from app.models.strategy import Strategy
from app.models.subscription import Subscription
from app.models.user import User

# Filters
from app.utils import filters

from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
celery = make_celery(app)

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler("error_log.txt")
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

