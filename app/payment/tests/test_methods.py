from unittest import TestCase

from app.payment.methods import (
    PayPaymentMethod,
    BillPaymentMethod,
    InvoicePaymentMethod,
    create_payment_method,
)
from app.payment.settings import CurrencyCode


class TestPaymentFactoryMethod(TestCase):
    def test_create_payment_method(self):
        sub_cases = [
            (CurrencyCode.EUR, PayPaymentMethod),
            (CurrencyCode.USD, BillPaymentMethod),
            (CurrencyCode.RUB, InvoicePaymentMethod),
        ]

        for currency_case, expected in sub_cases:
            with self.subTest(currency=currency_case):
                self.assertIsInstance(
                    create_payment_method(10, currency_case, "test"), expected
                )
