# файл: management/commands/load_test_data.py

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

from quiz.models import AnswersQuiz, TelegramQuiz
from users.models import User


class Command(BaseCommand):
    help = "Добавление тестовых данных: 2 пользователя и фикстура с викторинами"

    def handle(self, *args, **kwargs):
        TelegramQuiz.objects.all().delete()
        AnswersQuiz.objects.all().delete()
        list_delete_users = ["maria@example.com", "alex@example.com"]
        for email_user in list_delete_users:
            User.objects.filter(email=email_user).all().delete()
        call_command("loaddata", "fixture_users.json")
        call_command("loaddata", "fixture_poll.json")
        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены"))
