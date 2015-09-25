from app.models.strategy import Strategy

from flask import Blueprint, render_template

strategy = Blueprint('strategy', __name__)

@strategy.route('/strategies')
def strategies():
    strats = Strategy.query.all()
    return render_template('strategy/strategies.html', strats=strats)

@strategy.route('/strategies/<strategy_name>')
def strategy_details(strategy_name):
    # TODO This might be an inefficent query, can probably make it faster?
    # Maybe we cache the query in strategies function
    strategy_name = strategy_name.replace('-', ' ')
    # inEfficent query?
    strat = Strategy.query.filter(Strategy.name.ilike(strategy_name)).first()
    return render_template('strategy/details.html', strat=strat)
