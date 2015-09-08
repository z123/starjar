from flask import render_template

from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/strategies')
def strategies():
    return render_template('strategies.html')

@app.route('/strategies/<strategy_name>')
def strategy_details(strategy_name):
    # TODO Pass in strat info
    return render_template('strategy-details.html')


