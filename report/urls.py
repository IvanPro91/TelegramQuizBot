from django.urls import path

from report.apps import ReportConfig
from report.views import UserAnswersReportView

app_name = ReportConfig.name

urlpatterns = [
    path("", UserAnswersReportView.as_view(), name="report"),
]
