import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from quiz.forms import TelegramQuizFromCreate
from quiz.models import AnswersQuiz, TelegramQuiz


class QuizListView(LoginRequiredMixin, ListView):
    """Отображает список викторин текущего пользователя с пагинацией."""

    model = TelegramQuiz
    template_name = "main_quiz.html"
    context_object_name = "list_quiz"
    paginate_by = 10

    def get_queryset(self):
        user: TelegramQuiz = self.request.user
        return TelegramQuiz.objects.filter(user=user.pk)


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    """Обрабатывает удаление викторины через модальное окно."""

    model = TelegramQuiz
    template_name = "modal/modal_delete_quiz.html"
    context_object_name = "quiz"
    success_url = reverse_lazy("quiz:main")


class QuizUpdateView(LoginRequiredMixin, UpdateView):
    """Позволяет редактировать существующую викторину и её ответы через модальное окно."""

    model = TelegramQuiz
    form_class = TelegramQuizFromCreate
    template_name = "modal/modal_edit_quiz.html"
    context_object_name = "quiz"
    success_url = reverse_lazy("quiz:main")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz: TelegramQuiz = self.get_object()
        get_all_answers = quiz.answers.all()
        context["get_all_answers"] = get_all_answers
        return context

    def form_valid(self, form):
        quiz: TelegramQuiz = form.save(commit=False)
        quiz.answers.all().delete()

        if "answers" in self.request.POST:
            answers = json.loads(self.request.POST["answers"])
            chk_true_answer = any([answer["right_answer"] for answer in answers])
            if chk_true_answer:
                quiz.save()
                for answer in answers:
                    name = answer["name"]
                    right_answer = answer["right_answer"]
                    AnswersQuiz.objects.create(
                        name=name, quiz=quiz, right_answer=right_answer
                    )
        return super().form_valid(form)


class QuizCreateView(LoginRequiredMixin, CreateView):
    """Позволяет создать новую викторину с вариантами ответов через модальное окно."""

    model = TelegramQuiz
    template_name = "modal/modal_create_quiz.html"
    form_class = TelegramQuizFromCreate
    success_url = reverse_lazy("quiz:main")

    def form_valid(self, form):
        quiz: TelegramQuiz = form.save(commit=False)
        user = self.request.user
        quiz.user = user
        if "answers" in self.request.POST:
            answers = json.loads(self.request.POST["answers"])
            chk_true_answer = any([answer["right_answer"] for answer in answers])
            if chk_true_answer:
                quiz.save()
                for answer in answers:
                    name = answer["name"]
                    right_answer = answer["right_answer"]
                    AnswersQuiz.objects.create(
                        name=name, quiz=quiz, right_answer=right_answer
                    )
        return super().form_valid(form)
