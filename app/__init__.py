from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')

app.config.from_pyfile('config.py')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

# Views
from .views.page import page
app.register_blueprint(page)

# Models
from app.models import strategy, user
