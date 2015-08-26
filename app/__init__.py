from flask import Flask

app = Flask(__name__)
app.config.from_object('config.default')

from app.views import index 
