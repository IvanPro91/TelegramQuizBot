import random

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя, заменяющая стандартную модель.

    Вместо поля `username` используется `email` как уникальный идентификатор
    для аутентификации. Позволяет хранить дополнительную информацию о пользователе
    """

    username = models.CharField(max_length=200, null=True, blank=True)

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Введите почту",
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(verbose_name="Создание пользователя", auto_now_add=True)
    avatar = models.ImageField(upload_to="users/avatar", verbose_name="Аватар", null=True, blank=True)
    code = models.IntegerField(verbose_name="Код для подтверждения", default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @classmethod
    def create_user(cls, first_name: str, last_name: str, email: str, password: str) -> tuple[bool, "User"]:
        new_user = False
        user: "User" = cls.objects.filter(email=email).first()
        if not user:
            new_user = True
            user: "User" = cls.objects.create(first_name=first_name, last_name=last_name, email=email)
            user.code = random.randint(100000, 999999)
            user.is_active = False
            user.set_password(password)
            user.save()
        return new_user, user

    def __str__(self):
        return self.email

    def get_lazy_username(self):
        return f"{self.first_name[0]}{self.last_name[0]}"

    class Meta:
        """
        Определяет человекочитаемое имя модели и его множественную форму
        для отображения в интерфейсе администратора.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
