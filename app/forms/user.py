from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from app.models.user import User, db
from app.utils.validators import Unique

class LoginForm(Form):
    email = TextField('Email', [DataRequired(), Email(), Length(5, 64)])
    password = PasswordField('Password', [DataRequired(), Length(1, 128)])

class SignupForm(Form):
    email = TextField('Email', [DataRequired(),
                                Email(),
                                Length(5, 64),
                                Unique( User.email)])
                                 
    password = PasswordField('Password', [DataRequired(), Length(1, 128)])

class EmailForm(Form):
    email = TextField('Email', [DataRequired(), Email(), Length(5, 64)])
