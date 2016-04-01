from app.models.strategy import Strategy
from app import db

if db.engine.dialect.has_table(db.engine.connect(), 'strategies') and Strategy.query.get(1):
    STANDARD_PLAN_ID = Strategy.query.get(1).plan_id
else:
    STANDARD_PLAN_ID = None

