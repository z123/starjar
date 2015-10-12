from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from app.forms.user import LoginForm, SignupForm, EmailForm

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()

        if u and u.is_correct_password(form.password.data):
            login_user(u)
            return redirect(url_for('user.subscriptions'))
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
            return redirect(url_for('page.home'))

    return render_template('user/signup.html', form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.home'))

@user.route('/subscriptions')
@login_required
def subscriptions():
    # TODO: Logic for getting subscriptions
    return render_template('user/subscriptions.html')

@user.route('/reset-password', methods=['GET', 'POST'])
def password_reset():
    form = EmailForm()

    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        # TODO: Verify user exists and send Email

    return render_template('user/reset_password.html')

@user.route('/reset-password/<token>')
def reset_password_with_token():
    # TODO: Insert resetting logic
    return render_template('user/reset_password_with_token.html')
