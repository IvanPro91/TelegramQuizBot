from django.shortcuts import render
from django.urls import path

from marketing.apps import MarketingConfig

app_name = MarketingConfig.name

urlpatterns = [
    path("", lambda x: render(x, "page_marketing.html"), name="marketing"),
]
