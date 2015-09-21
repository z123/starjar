from app import db
from app.models.strategy import Strategy
from app.models.user import User


def create_admin():
    params = {
        'role': 'admin',
        'email': 'admin@starjar.com',
        'password': 'password'
    }

    return User(**params).save()

def create_strategies():
    params = {
        'name': "The banana sunde",
        'description': "This strategy rocks",
        'quantopian_url': "http://www.quantopian.com"
    }

    return Strategy(**params).save()

def seed():
    """Seeds database with dummy data."""
    create_admin()
    create_strategies()

def reset():
    db.drop_all()
    db.create_all()
    seed()

