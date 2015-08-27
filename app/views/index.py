from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/strategies')
def strategies():
    return render_template('strategies.html')
