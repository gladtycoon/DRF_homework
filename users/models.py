from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=150, verbose_name="Имя", help_text="Укажите свое имя"
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", help_text="Укажите свою фамилию"
    )
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите свою почту"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите свой город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="avatar",
        help_text="Загрузите аватарку",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Наличные"
        TRANSFER = "transfer", "Перевод на счет"

    payment_user = models.ForeignKey(
        User,  # лучше использовать гибкую модель: settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
        blank=True,
        null=True,
    )

    payment_date = models.DateField(
        verbose_name="Дата платежа",  # можно воткнуть auto_now_add=True, или auto_now =True,
        help_text="Укажите дату платежа",
        blank=True,
        null=True,
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Оплаченный курс",
        blank=True,
        null=True,
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Урок",
        help_text="Оплаченный урок",
        blank=True,
        null=True,
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.TRANSFER,
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.payment_user} - {self.amount} ({self.payment_date})"
