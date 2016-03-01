from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from wtforms.validators import ValidationError
from flask_login import current_user

from app.models.user import User, db
from app.utils.validators import Unique

class LoginForm(Form):
    email = TextField('Email', [Length(0, 64)])
    password = PasswordField('Password', [Length(0, 128)])

class UpdateAccountForm(Form):
    email = TextField('Email', [DataRequired(message="Email address required"),
                                Email(message="Not a valid email address"),
                                Length(max=128, message="The email address must be under 128 \
                                                        characters")])
    new_password = PasswordField('Password', [Length(0, 128)])
    current_password = PasswordField('Password', [Length(0, 128)])

    def validate_email(form, field):
        check = User.email.class_.query.filter(User.email == field.data).first()
        if check and current_user.email != field.data:
            raise ValidationError("That email is already in use.")

class SignupForm(Form):
    email = TextField('Email', [DataRequired(message="Email address required"),
                                Email(message="Not a valid email address"),
                                Length(max=128, message="The email address must be under 128 \
                                                        characters"),
                                Unique(User.email, message="That email is already in use")])
                                 
    password = PasswordField('Password', [DataRequired(message="Password field required"),
                                          Length(max=128, message="Password must be under 128 \
                                                                  characters")])

class EmailForm(Form):
    email = TextField('Email')

class PasswordForm(Form):
    password = PasswordField('Password', [DataRequired(message="Password field required"),
                                          Length(max=128, message="Password must be under 128 \
                                                                  characters")])

class EmptyForm(Form):
    pass
