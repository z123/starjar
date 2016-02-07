from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

page = Blueprint('page', __name__)

@page.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('user.subscriptions'))
    return render_template('home.html')

@page.route('/about')
def about():
    return render_template('about.html')

@page.route('/faq')
def faq():
    return render_template('faq.html')

@page.route('/blog')
def blog():
    return render_template('blog.html')


