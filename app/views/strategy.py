from app import db
from app.models.strategy import Strategy

from flask import Blueprint, render_template

strategy = Blueprint('strategy', __name__)

@strategy.route('/strategies')
def strategies():
    strats = Strategy.query.all()
    return render_template('strategies.html', strats=strats)

@strategy.route('/strategies/<strategy_name>')
def strategy_details(strategy_name):
    # TODO Pass in strat info
    return render_template('strategy-details.html')
