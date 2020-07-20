import os
from enum import Enum


class CurrencyCode(Enum):
    EUR = 978
    USD = 840
    RUB = 643


PIASTRIX_PAY_URL_RU = "https://pay.piastrix.com/ru/pay"
PIASTRIX_PAY_URL_EN = "https://pay.piastrix.com/en/pay"
PIASTRIX_BILL_URL = "https://core.piastrix.com/bill/create"
PIASTRIX_INVOICE_URL = "https://core.piastrix.com/invoice/create"

INVOICE_PAYWAY = "payeer_rub"

SECRET_KEY_PAYMENT = os.environ.get("SECRET_KEY_PAYMENT", "SecretKey01")
SHOP_ID = os.environ.get("SHOP_ID", 5)
