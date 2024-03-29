from flask import (
    abort,
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import current_user, login_user, login_required, logout_user
from app import app
from app import mail
from app.models.user import User
from app.forms.user import LoginForm, SignupForm, EmailForm, PasswordForm, UpdateAccountForm, EmptyForm
from app.utils.security import ts
from app.utils.constants import STANDARD_PLAN_ID
from flask_mail import Message
import requests

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.subscription'))

    form = LoginForm()

    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data.lower()).first()

        if u and u.is_correct_password(form.password.data):
            login_user(u)
            return redirect(url_for('user.subscription'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('user/login.html', form=form)

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        u = User()

        form.populate_obj(u)
        u.email = form.email.data.lower()
        u.password = form.password.data

        u.save()

        if login_user(u):
            return redirect(url_for('user.subscription'))
    elif len(form.errors):
        flash(form.errors.values()[0][0], 'error')

    return render_template('user/signup.html', form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.home'))

@user.route('/subscription')
@login_required
def subscription():
    if current_user.is_subscribed(STANDARD_PLAN_ID) or current_user.role == 'admin':
        return render_template('user/subscription.html')
    else:
        return redirect(url_for('billing.subscribe'))

# @user.route('/subscriptions')
# @login_required
# def subscriptions():
    # return render_template('user/subscriptions.html', subscriptions=current_user.subscriptions)

@user.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = EmailForm()

    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u:
            flash('A password reset email has been sent.')
            subject = 'Password reset requested'
            token = ts.dumps(u.email, salt='recover-key')
            reset_url = url_for('user.password_reset', token=token, _external=True)
            # TODO: Change email/recover to something else like email/reset_password
	    html = render_template('email/recover.html', reset_url=reset_url)
            # SMTP
            # msg = Message(subject, [u.email], html=html, sender=("EquityBuilder", "no-reply@equitybuilder.io"))
            # mail.send(msg)
            # API
	    requests.post(app.config.get('MAILGUN_API_BASE_URL'),
		auth=("api", app.config.get('MAILGUN_API_KEY')),
		data={"from": "EquityBuilder <no-reply@equitybuilder.io>",
		      "to": [u.email],
		      "subject": "Password Reset Requested",
		      "html": html})
        else:
            flash('No user under that email exists.')

    return render_template('user/forgot_password.html', form=form)

@user.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=email).first_or_404()
        u.password = form.password.data
        u.save()

        return redirect(url_for('user.login'))
    elif len(form.errors):
            flash(form.errors.values()[0][0], 'error')

    return render_template('user/password_reset.html', form=form, token=token)

@user.route('/settings/account', methods=['GET', 'POST'])
@login_required
def account_settings():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if current_user.is_correct_password(form.current_password.data):
            current_user.email = form.email.data
            if len(form.new_password.data):
                current_user.password = form.new_password.data
            current_user.save()
            flash("Account settings updated.")
        else:
            flash("Incorrect password.", 'error')
    elif len(form.errors):
        flash(form.errors.values()[0][0], 'error')

    return render_template('user/settings.html', form=form, settings='account')

@user.route('/settings/subscription', methods=['GET', 'POST'])
@login_required
def subscription_settings():
    form = EmptyForm()
    if form.validate_on_submit():
        #TODO: Put this plan in a constant somewhere.
        if current_user.cancel(STANDARD_PLAN_ID):
            flash("Your subscription has been canceled.")
        else:
            flash("You currently don't have a subscription.")

    elif len(form.errors):
        flash(form.errors.values()[0][0], 'error')

    return render_template('user/settings.html', form=form, settings='subscription')


