from django.shortcuts import render
from django.urls import path

from report.apps import ReportConfig

app_name = ReportConfig.name

urlpatterns = [
    path("", lambda x: render(x, "page_report.html"), name="report"),
]
