from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import login_user
from app.models.user import User
from app.forms.user import LoginForm, SignupForm

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()

        if u and u.is_correct_password(form.password.data):
            login_user(u)
            return redirect(url_for('page.home'))
        else:
            flash('Email or password is incorrect.', 'error')

    return render_template('user/login.html', form=form)

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        u = User()

        form.populate_obj(u)
        u.password = request.form.get('password')

        u.save()

        if login_user(u):
            flash('Awesome, thanks for signing up!', 'success')
            next_ = request.args.get('next')
            return redirect(next_ or url_for('page.home'))

    return render_template('user/signup.html', form=form)

    
