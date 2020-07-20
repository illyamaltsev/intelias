from abc import ABC, abstractmethod

import logging
import requests
from flask import render_template, redirect

from app.payment import settings
from app.payment.settings import CurrencyCode
from app.payment.sign import SignGenerator

logger = logging.getLogger("app")


class MethodRequestResponseError(Exception):
    pass


class APaymentMethod(ABC):

    @abstractmethod
    def do_payment(self):
        pass


class PaymentMethodBase(APaymentMethod):
    def __init__(
            self, amount: float,
            currency: int,
            description: str,
            shop_order_id: int
    ):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.shop_order_id = shop_order_id

    @abstractmethod
    def do_request(self):
        pass

    @abstractmethod
    def get_required_keys(self):
        pass

    def sign(self, sign_data):
        if not set(sign_data) == set(self.get_required_keys()):
            logger.fatal(f"sign_data keys is not equal to required keys")
        sg = SignGenerator(sign_data, settings.SECRET_KEY_PAYMENT)
        return sg.generate()

    def process_response(self, response):
        return response

    def do_payment(self):
        response = self.do_request()

        logger.info(f"{self.__class__.__name__} get response {response}")

        processed_response = self.process_response(response)

        logger.info(f"{self.__class__.__name__} process response "
                    f"{processed_response}")
        return processed_response


class PayPaymentMethod(PaymentMethodBase):
    __sign_required_keys = ["amount", "currency", "shop_id", "shop_order_id"]

    def get_required_keys(self):
        return self.__sign_required_keys

    def do_request(self):
        sign_data = {
            "amount": self.amount,
            "currency": self.currency,
            "shop_id": settings.SHOP_ID,
            "shop_order_id": self.shop_order_id,
        }

        data = {
            "method": "post",
            "url": settings.PIASTRIX_PAY_URL_RU,
            "amount": self.amount,
            "currency": self.currency,
            "shop_id": settings.SHOP_ID,
            "sign": self.sign(sign_data),
            "shop_order_id": self.shop_order_id,
            "description": self.description,
        }

        logger.info(f"{self.__class__.__name__} do_request with {data}")

        return data

    def process_response(self, response):
        return render_template("piastrix/pay.html", data=response)


class BillPaymentMethod(PaymentMethodBase):
    __sign_required_keys = [
        "shop_amount", "shop_currency", "shop_id", "shop_order_id",
        "payer_currency",
    ]

    def get_required_keys(self):
        return self.__sign_required_keys

    def do_request(self):
        data = {
            "shop_amount": self.amount,
            "shop_currency": self.currency,
            "shop_id": settings.SHOP_ID,
            "shop_order_id": self.shop_order_id,
            "payer_currency": self.currency,
        }

        data["sign"] = self.sign(data)

        logger.info(f"{self.__class__.__name__} do_request with {data}")

        response = requests.post(settings.PIASTRIX_BILL_URL, json=data)
        response = response.json()
        return response

    def process_response(self, response):
        if response["result"]:
            url_for_redirect = response["data"]["url"]
            return redirect(url_for_redirect)
        else:
            raise MethodRequestResponseError(response["message"])


class InvoicePaymentMethod(PaymentMethodBase):
    __sign_required_keys = ["amount", "currency", "payway", "shop_id",
                            "shop_order_id"]

    def get_required_keys(self):
        return self.__sign_required_keys

    def do_request(self):
        data = {
            "amount": self.amount,
            "currency": self.currency,
            "payway": settings.INVOICE_PAYWAY,
            "shop_id": settings.SHOP_ID,
            "shop_order_id": self.shop_order_id,
        }

        data["sign"] = self.sign(data)

        logger.info(f"{self.__class__.__name__} do_request with {data}")

        response = requests.post(settings.PIASTRIX_INVOICE_URL, json=data)
        response = response.json()
        return response

    def process_response(self, response):
        if response["result"]:
            response_data = response["data"]
            response_details = response_data["data"]

            context = {
                "url": response_data["url"],
                "method": response_data["method"],
                "lang": "ru",
                "m_curorderid": response_details["m_curorderid"],
                "m_historyid": response_details["m_historyid"],
                "m_historytm": response_details["m_historytm"],
                "referer": response_details["referer"],
            }

            return render_template("piastrix/invoice.html", data=context)
        else:
            raise MethodRequestResponseError(response["message"])


def create_payment_method(
        amount: float,
        currency_code: CurrencyCode,
        description: str,
        shop_order_id: int
) -> APaymentMethod:
    """PaymentMethod factory method.
    It creates needed method according to currency_code
    """

    method_class = None
    if currency_code == CurrencyCode.EUR:
        method_class = PayPaymentMethod
    elif currency_code == CurrencyCode.USD:
        method_class = BillPaymentMethod
    elif currency_code == CurrencyCode.RUB:
        method_class = InvoicePaymentMethod
    return method_class(amount, currency_code.value, description,
                        shop_order_id)
