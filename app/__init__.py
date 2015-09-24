from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')

app.config.from_pyfile('config.py')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'user.signup'

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=app.config.get('BT_MERCHANT_ID'),
                                  public_key=app.config.get('BT_PUBLIC_KEY'),
                                  private_key=app.config.get('BT_PRIVATE_KEY'))

# Views
from app.views.page import page
from app.views.strategy import strategy
from app.views.user import user
from app.views.billing import billing

app.register_blueprint(page)
app.register_blueprint(strategy)
app.register_blueprint(user)
app.register_blueprint(billing)

# Models
from app.models.user import User
from app.models.strategy import Strategy

# Filters
from app.utils import filters
