from unittest import TestCase

from app.payment.sign import SignGenerator


class TestSignGenerator(TestCase):
    def test_generate(self):
        data_case = {
            "currency": "643",
            "payway": "payeer_rub",
            "amount": "12.34",
            "shop_id": "5",
            "shop_order_id": 4126,
        }

        secret_key_case = "SecretKey01"

        sg = SignGenerator(data_case, secret_key_case)

        self.assertEqual(
            sg.generate(),
            "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1",
        )
