from django.shortcuts import render
from django.urls import path

from rating.apps import RatingConfig

app_name = RatingConfig.name

urlpatterns = [
    path("", lambda x: render(x, "page_rating.html"), name="rating"),
]
