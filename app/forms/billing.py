from flask_wtf import Form
from wtforms import TextField, HiddenField
from wtforms.validators import DataRequired, Length

class PaymentForm(Form):
    # Can't use fields with braintree attributes in them
    # braintree does something to the fields which causes
    # validation to fail.
    #credit_card = TextField('Credit Card', [DataRequired()])
    #cvv = TextField('CVV', [DataRequired()])
    #expiration_date = TextField('Expiration Date', [DataRequired()])

    plan_id = HiddenField(validators=[DataRequired(), Length(1, 128)])

