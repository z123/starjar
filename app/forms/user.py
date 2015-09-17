from flask.ext.wtforms import Form
from wtforms import TextField, PasswordField, DataRequired

class LoginForm(Form):
    email = TextField('Email', [DataRequired(), Length(5, 254)])
    password = PasswordField('Password', [DataRequired(), Length(1, 128)])
