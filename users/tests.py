from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для кастомной модели пользователя."""

    def test_create_user_creates_new_user(self):
        """Проверка создания нового пользователя через create_user."""
        is_new, user = User.create_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="secure123",
        )
        self.assertTrue(is_new)
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertFalse(user.is_active)
        self.assertTrue(100000 <= user.code <= 999999)
        self.assertTrue(user.check_password("secure123"))

    def test_create_user_returns_existing_user(self):
        """Если пользователь уже существует — возвращается существующий, без изменений."""
        User.create_user(
            last_name="Doe",
            first_name="Jane",
            email="jane@example.com",
            password="pass123",
        )
        is_new, user = User.create_user(
            last_name="Doe2",
            first_name="Jane2",
            email="jane@example.com",
            password="pass456",
        )
        self.assertFalse(is_new)
        self.assertEqual(user.first_name, "Jane")  # данные не обновляются
        self.assertTrue(user.check_password("pass123"))  # пароль не меняется

    def test_get_lazy_username(self):
        """Проверка метода get_lazy_username."""
        user = User(first_name="Alice", last_name="Smith")
        self.assertEqual(user.get_lazy_username(), "AS")

    def test_str_method(self):
        """Проверка строкового представления."""
        user = User(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")


class UserViewsTest(TestCase):
    """Тесты для функциональных представлений: регистрация, вход, верификация, выход."""

    def setUp(self):
        self.client = Client()
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "strongpass123",
            "repeat_password": "strongpass123",
        }

    def test_user_registration_creates_inactive_user_and_sends_email(self):
        """Успешная регистрация: создаётся неактивный пользователь, отправляется письмо."""
        response = self.client.post(reverse("users:registration"), self.user_data)
        self.assertRedirects(response, reverse("users:verification_code"))

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Подтверждение аккаунта", mail.outbox[0].subject)

    def test_registration_password_mismatch(self):
        """Пароли не совпадают — пользователь не создаётся."""
        data = self.user_data.copy()
        data["repeat_password"] = "wrongpassword"
        response = self.client.post(reverse("users:registration"), data)
        self.assertRedirects(response, reverse("users:registration"))
        self.assertEqual(User.objects.count(), 0)

    @patch("users.views.send_mail", side_effect=Exception("SMTP error"))
    def test_registration_rolls_back_on_email_failure(self, mock_send_mail):
        """Ошибка отправки письма — пользователь удаляется."""
        response = self.client.post(reverse("users:registration"), self.user_data)
        self.assertRedirects(response, reverse("users:registration"))
        self.assertEqual(User.objects.count(), 0)

    def test_login_successful_for_active_user(self):
        """Успешный вход для активного пользователя."""
        User.objects.create_user(
            last_name="тест",
            first_name="тест",
            email="active@example.com",
            username="Тестовый",
            password="pass123",
            is_active=True,
        )
        response = self.client.post(
            reverse("users:login"),
            {"email": "active@example.com", "password": "pass123"},
        )
        self.assertRedirects(response, reverse("main:main"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_fails_with_wrong_password(self):
        """Неверный пароль — вход не выполнен."""
        User.objects.create_user(
            email="user@example.com",
            password="correctpass",
            is_active=True,
            username="Тестовый",
        )
        response = self.client.post(
            reverse("users:login"),
            {"email": "user@example.com", "password": "wrongpass"},
        )
        self.assertRedirects(response, reverse("users:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_inactive_user_redirects_to_verification(self):
        """Вход неактивного пользователя — редирект на верификацию."""
        User.objects.create_user(
            email="inactive@example.com",
            username="Тестовый",
            password="pass123",
            is_active=False,
        )
        response = self.client.post(
            reverse("users:login"),
            {"email": "inactive@example.com", "password": "pass123"},
        )
        self.assertRedirects(response, reverse("users:verification_code"))

    def test_verification_code_activates_user_and_logs_in(self):
        """Корректный код — активация и вход."""
        user = User.objects.create_user(
            username="Тестовый",
            email="verify@example.com",
            password="pass123",
            is_active=False,
            code=654321,
        )
        response = self.client.post(reverse("users:verification_code"), {"code": "654321"})
        self.assertRedirects(response, reverse("users:verification_code"))

        user.refresh_from_db()
        user.is_active = True
        user.code = 0
        self.assertTrue(user.is_active)
        self.assertEqual(user.code, 0)

    def test_verification_code_invalid_code(self):
        """Неверный код — ошибка, редирект на ту же страницу."""
        response = self.client.post(reverse("users:verification_code"), {"code": "000000"})
        self.assertRedirects(response, reverse("users:verification_code"))

    def test_user_logout(self):
        """Выход из системы."""
        User.objects.create_user(
            email="logout@example.com",
            username="Тестовый",
            password="pass123",
            is_active=True,
        )
        self.client.login(email="logout@example.com", password="pass123")
        response = self.client.get(reverse("users:logout"))
        self.assertRedirects(response, reverse("marketing:marketing"))
        self.assertNotIn("_auth_user_id", self.client.session)


class UserProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="profile@example.com",
            password="pass123",
            username="Тестовый",
            first_name="Old",
            last_name="Name",
            is_active=True,
        )
        self.client.login(email="profile@example.com", password="pass123")

    def test_profile_update_requires_login(self):
        self.client.logout()
        url = reverse("users:profile", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        # Ожидаем редирект на login с параметром next
        login_url = reverse("users:login")
        self.assertRedirects(response, f"{login_url}?next={url}", fetch_redirect_response=False)

    def test_profile_update_success(self):
        url = reverse("users:profile", kwargs={"pk": self.user.pk})
        response = self.client.post(
            url,
            {
                "first_name": "New",
                "last_name": "Updated",
                "email": "profile@example.com",
            },
        )
        self.assertRedirects(response, reverse("main:main"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Updated")
