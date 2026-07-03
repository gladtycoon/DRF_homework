from django.contrib.auth.models import AbstractUser
from django.db import models


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
