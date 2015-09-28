from flask_wtf import Form
from wtforms import TextField, HiddenField
from wtforms.validators import DataRequired, Length

class PaymentForm(Form):
    credit_card = TextField('Credit Card', [DataRequired()])
    cvv = TextField('CVV', [DataRequired()])
    expiration_date = TextField('Expiration Date', [DataRequired()])

    plan_id = HiddenField(validators=[DataRequired(), Length(1, 128)])

