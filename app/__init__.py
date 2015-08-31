from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Views
from app.views import index 

# Models
from app.models import strategy
