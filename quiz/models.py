from django.db import models

from telegram_bot.models import TelegramUser
from users.models import User


class TelegramQuiz(models.Model):
    """Модель викторины, созданной пользователем, с вопросом, подсказкой и статистикой."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_quiz")
    quest = models.CharField(max_length=300)
    hint = models.TextField()

    count_current_answer = models.PositiveIntegerField(default=0)
    count_wrong_answer = models.PositiveIntegerField(default=0)
    count_view_answer = models.PositiveIntegerField(default=0)

    feedback_wrong = models.PositiveIntegerField(default=0)
    feedback_like = models.PositiveIntegerField(default=0)
    feedback_dislike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quest}"

    class Meta:
        verbose_name = "Викторина"
        verbose_name_plural = "Викторины"


class AnswersQuiz(models.Model):
    """Модель варианта ответа на вопрос викторины, с указанием правильности."""

    name = models.CharField(max_length=100)
    quiz = models.ForeignKey(
        TelegramQuiz, on_delete=models.CASCADE, related_name="answers"
    )
    right_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.right_answer}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class FeedbackQuiz(models.Model):
    """Модель фиксации факта оставленной пользователем обратной связи по викторине."""

    quiz = models.ForeignKey(TelegramQuiz, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.telegram_user}"

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"


class PollUserSending(models.Model):
    """Модель фиксации факта пройденной викторины."""

    id_quiz = models.TextField()
    quiz_user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(TelegramQuiz, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    current_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.telegram_user}"

    class Meta:
        verbose_name = "Отправленная викторина"
        verbose_name_plural = "Отправленные викторины"
