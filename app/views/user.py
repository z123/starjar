from app.models.user import User
from app.forms.user import LoginForm
from flask import Blueprint, render_template

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    pass

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    pass
