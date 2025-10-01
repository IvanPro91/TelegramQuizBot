from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path

from main.apps import MainConfig
from main.views import TelegramUserQuizListView

app_name = MainConfig.name

urlpatterns = [
    path("", TelegramUserQuizListView.as_view(), name="main"),
]
