from flask import Blueprint, render_template

strategy = Blueprint('strategy', __name__)

@strategy.route('/strategies')
def strategies():
    return render_template('strategies.html')

@strategy.route('/strategies/<strategy_name>')
def strategy_details(strategy_name):
    # TODO Pass in strat info
    return render_template('strategy-details.html')
