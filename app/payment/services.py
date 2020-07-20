import logging

from app.payment.methods import create_payment_method
from app.payment.models import Order, db
from app.payment.settings import CurrencyCode

logger = logging.getLogger("app")


def do_payment(
        amount: float,
        currency_code: CurrencyCode,
        description: str
):
    logger.info(
        f"Incoming payment with amount={amount}, "
        f"currency={currency_code}, description={description}"
    )

    new_order = Order(amount=amount, currency=currency_code,
                      description=description)

    db.session.add(new_order)
    db.session.commit()

    method = create_payment_method(amount, currency_code, description,
                                   new_order.id)
    logger.debug(f"Created payment method class {type(method).__name__}")
    return method.do_payment()
