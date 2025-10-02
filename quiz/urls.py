from django.urls import path

from quiz.apps import QuizConfig
from quiz.views import QuizCreateView, QuizDeleteView, QuizListView, QuizUpdateView

app_name = QuizConfig.name

urlpatterns = [
    path("", QuizListView.as_view(), name="main"),
    path("create_quiz/", QuizCreateView.as_view(), name="create_quiz"),
    path("edit_quiz/<int:pk>", QuizUpdateView.as_view(), name="edit_quiz"),
    path("delete_quiz/<int:pk>", QuizDeleteView.as_view(), name="delete_quiz"),
]
