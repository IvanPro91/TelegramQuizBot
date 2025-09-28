from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path

from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path("", lambda x: render(x, "page_main.html"), name="main"),
]
