from app import db
from app.models.strategy import Strategy
from app.models.user import User


def create_admin():
    params = {
        'role': 'admin',
        'email': 'support@equitybuilder.io',
        'password': 'bibirkobr'
    }

    return User(**params).save()

def create_strategies():
    params = {
        'name': "Standard strategy",
        'description': "",
        'quantopian_url': "https://www.quantopian.com/algorithms/56d884653e72f1938700082d",
        'plan_id': "standard-plan"
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


