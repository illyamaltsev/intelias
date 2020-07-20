from wtforms import FloatField, SelectField, TextAreaField
from wtforms import Form
from wtforms.validators import InputRequired, NumberRange

from app.payment.settings import CurrencyCode


class PaymentForm(Form):

    amount = FloatField(
        label="Amount", validators=[InputRequired(), NumberRange(min=1)]
    )

    currency = SelectField(
        label="Currency",
        choices=list((str(x.value), x.name) for x in CurrencyCode),
        validators=[InputRequired()],
    )

    description = TextAreaField("Description")
