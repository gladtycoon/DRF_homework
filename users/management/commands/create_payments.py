from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    help = "Создает тестовые платежи"

    def handle(self, *args, **kwargs):
        # Создаём пользователя, если нет
        user, created = User.objects.get_or_create(
            email="admin@email.com",
            defaults={
                "is_superuser": True,
                "is_staff": True,
                "password": "pbkdf2_sha256$260000$...",  # можно просто set_password
            },
        )
        if created:
            user.set_password("admin123")
            user.save()
            self.stdout.write("Пользователь создан")

        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payments.objects.get_or_create(
            payment_user=user,
            paid_course=course,
            defaults={
                "payment_date": "2026-07-01",
                "amount": 1000.00,
                "payment_method": "transfer",
            },
        )

        Payments.objects.get_or_create(
            payment_user=user,
            paid_lesson=lesson,
            defaults={
                "payment_date": "2026-07-02",
                "amount": 500.00,
                "payment_method": "cash",
            },
        )

        self.stdout.write(self.style.SUCCESS("Платежи созданы"))
