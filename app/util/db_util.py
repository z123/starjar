from app.models.strategy import Strategy
from app import db


def create_strategies():
    params = {
        'name': "The banana sunde",
        'description': "This strategy rocks",
        'quantopian_url': "http://www.quantopian.com"
    }

    return Strategy(**params).save()

def seed():
    """Seeds database with dummy data."""
    create_strategies()

def reset():
    pass

    
