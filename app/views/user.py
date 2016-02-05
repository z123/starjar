from flask import (
    Blueprint,
    flash,
    url_for,
    redirect,
    request,
    render_template)
from flask_login import current_user, login_user, login_required, logout_user
from app import mail
from app.models.user import User
from app.forms.user import LoginForm, SignupForm, EmailForm, PasswordForm, ChangeEmailForm
from app.utils.security import ts
from flask_mail import Message

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
            flash('Invalid email or password', 'error')

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
            flash('Thanks for signing up!', 'success')
            return redirect(url_for('user.subscriptions'))
    elif len(form.errors):
        flash(form.errors.values()[0][0], 'error')

    return render_template('user/signup.html', form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.home'))

@user.route('/subscriptions')
@login_required
def subscriptions():
    return render_template('user/subscriptions.html', subscriptions=current_user.subscriptions)

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
            msg = Message(subject, [u.email], html=html)
            mail.send(msg)
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

@user.route('/settings', methods=['GET', 'POST'])
def settings():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        pass
    return render_template('user/settings.html')
