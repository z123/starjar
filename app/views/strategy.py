# from app.models.strategy import Strategy

from flask import Blueprint, render_template
from flask_login import current_user

strategy = Blueprint('strategy', __name__)

# @strategy.route('/strategies')
# def strategies():
    # strats = Strategy.query.all()
    # return render_template('strategy/strategies.html', strats=strats)

@strategy.route('/strategy/<strategy_name>')
def strategy_details(strategy_name):
    # TODO This might be an inefficent query, can probably make it faster?
    # Maybe we cache the query in strategies function
    strategy_name = strategy_name.replace('-', ' ')
    # inEfficent query?
    strat = Strategy.query.filter(Strategy.name.ilike(strategy_name)).first()

    # TODO: Add a method to the user class that easily checks if 
    # a user is subscribed to a particular startegy, can save a lot of code :)

    # Check if current user is subscribed to strategy
    if current_user.is_authenticated():
        subscribed = current_user.is_subscribed(strat.plan_id)
    else:
        subscribed = False
        
    return render_template('strategy/details.html', strat=strat, subscribed=subscribed)
