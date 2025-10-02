from django.urls import path

from rating.apps import RatingConfig
from rating.views import UserRatingView

app_name = RatingConfig.name

urlpatterns = [
    path("", UserRatingView.as_view(), name="rating"),
]
