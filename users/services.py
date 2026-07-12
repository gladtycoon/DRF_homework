import requests
import stripe
from rest_framework import status

from config import settings
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует сумму оплаты в доллары."""
    response = requests.get(
        f"{settings.CUR_API_URL}v3/latest?apikey={settings.CUR_API_KEY}&currencies=RUB"
    )
    if response.status_code == status.HTTP_200_OK:
        usd_price = round(response.json()["data"]["RUB"]["value"], 1)
        return int(float(amount) / usd_price)
    return int(float(amount))  # исключаем ошибку в случае, если API не отдаст ответ


def create_stripe_course_for_payment(amount):
    """Создает в страйпе курс для оплаты."""

    product = stripe.Product.create(name="Курс для оплаты")
    return product.id


def create_stripe_price(amount, product_id):
    """Создает в страйпе цену, привязанную к курсу."""

    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id):
    """Создает в страйпе сессию на оплату курса."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url


def get_stripe_session_status(session_id):
    """Получает статус сессии оплаты по её ID."""

    session = stripe.checkout.Session.retrieve(session_id)
    return {"status": session.status, "payment_status": session.payment_status}
