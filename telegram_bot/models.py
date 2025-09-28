from django.db import models


class TelegramUser(models.Model):
    """Модель пользователя Telegram с основной профильной информацией."""

    id_user = models.TextField()
    username_user = models.TextField(null=True, blank=True)
    first_name_user = models.TextField(null=True, blank=True)
    last_name_user = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username_user} {self.first_name_user} {self.last_name_user}"

    class Meta:
        verbose_name = "телеграм пользователь"
        verbose_name_plural = "телеграм пользователи"
