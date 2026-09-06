import requests

from django.conf import settings


class ZarinpalService:

    REQUEST_URL = (
        "https://api.zarinpal.com/pg/v4/payment/request.json"
    )

    VERIFY_URL = (
        "https://api.zarinpal.com/pg/v4/payment/verify.json"
    )

    START_PAY_URL = (
        "https://www.zarinpal.com/pg/StartPay/"
    )

    def request_payment(self, payment):

        # مبلغ در دیتابیس بر حسب تومان است.
        # زرین‌پال مبلغ را بر حسب ریال دریافت می‌کند.
        amount_in_rial = payment.amount * 10

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount_in_rial,
            "description": (
                f"خرید دوره "
                f"{payment.order.course.title}"
            ),
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
        }

        response = requests.post(
            self.REQUEST_URL,
            json=data,
            timeout=15,
        )

        response.raise_for_status()

        return response.json()

    def verify_payment(self, payment):

        amount_in_rial = payment.amount * 10

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount_in_rial,
            "authority": payment.authority,
        }

        response = requests.post(
            self.VERIFY_URL,
            json=data,
            timeout=15,
        )

        response.raise_for_status()

        return response.json()

    def payment_url(self, authority):

        return f"{self.START_PAY_URL}{authority}"