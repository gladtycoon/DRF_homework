from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_inactive_users():
    """Блокирует пользователей, которые не заходили более месяца."""

    month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = users.update(is_active=False)
    if count == 1:
        msg = "Заблокирован 1 пользователь"
    elif count in [2, 3, 4]:
        msg = f"Заблокировано {count} пользователя"
    else:
        msg = f"Заблокировано {count} пользователей"
    return msg
