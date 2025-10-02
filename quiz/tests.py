import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.test import TestCase
from django.urls import reverse

from quiz.models import AnswersQuiz, TelegramQuiz

User = get_user_model()


class QuizViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com",
            username="test",
            password="12345",
            last_name="тест",
            first_name="тест",
        )
        self.other_user = User.objects.create_user(
            email="otheruser@test.com",
            username="test",
            password="12345",
            last_name="тест",
            first_name="тест",
        )

        self.quiz = TelegramQuiz.objects.create(
            user=self.user,
            quest="Какой самый большой океан?",
            hint="Подсказка: он синий и огромный",
        )
        self.answer1 = AnswersQuiz.objects.create(quiz=self.quiz, name="Тихий", right_answer=True)
        self.answer2 = AnswersQuiz.objects.create(quiz=self.quiz, name="Атлантический", right_answer=False)

    def login_user(self):
        self.client.login(email="testuser@test.com", password="12345")

    def test_quiz_list_view_requires_login(self):
        response = self.client.get(reverse("quiz:main"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_quiz_create_view_requires_login(self):
        response = self.client.get(reverse("quiz:create_quiz"))
        self.assertEqual(response.status_code, 302)

    def test_quiz_update_view_requires_login(self):
        response = self.client.get(reverse("quiz:edit_quiz", kwargs={"pk": self.quiz.pk}))
        self.assertEqual(response.status_code, 302)

    def test_quiz_delete_view_requires_login(self):
        response = self.client.get(reverse("quiz:delete_quiz", kwargs={"pk": self.quiz.pk}))
        self.assertEqual(response.status_code, 302)

    def test_quiz_delete_by_other_user_forbidden(self):
        self.client.login(email="otheruser@test.com", password="12345")
        response = self.client.post(reverse("quiz:delete_quiz", kwargs={"pk": self.quiz.pk}))

        self.assertRedirects(response, reverse("quiz:main"))

    def test_anonymous_user_cannot_access_any_quiz_view(self):
        urls = [
            reverse("quiz:main"),
            reverse("quiz:create_quiz"),
            reverse("quiz:edit_quiz", kwargs={"pk": self.quiz.pk}),
            reverse("quiz:delete_quiz", kwargs={"pk": self.quiz.pk}),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertFalse(response.url.startswith("/accounts/login/"))
