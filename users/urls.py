from django.urls import path

from users.apps import UsersConfig
from users.views import (UserProfileUpdateView, user_logout, users_login,
                         users_registration, verification_code)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", users_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/<int:pk>", UserProfileUpdateView.as_view(), name="profile"),
    path("registration/", users_registration, name="registration"),
    path("verification_code/", verification_code, name="verification_code"),
]
