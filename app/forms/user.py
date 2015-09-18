from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    email = TextField('Email', [DataRequired(), Length(5, 254)])
    password = PasswordField('Password', [DataRequired(), Length(1, 128)])
