from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views.generic import ListView

from quiz.models import AnswersQuiz, PollUserSending
from telegram_bot.models import TelegramUser


class UserAnswersReportView(LoginRequiredMixin, ListView):
    """Отчет по ответам пользователей на викторины."""
    template_name = "page_report.html"
    context_object_name = "user_answers"
    paginate_by = 25

    def get_queryset(self):
        """Возвращает ответы пользователей с предзагрузкой связанных данных."""
        queryset = (
            PollUserSending.objects.filter(quiz_user=self.request.user)
            .select_related("telegram_user", "quiz")
            .prefetch_related(Prefetch("quiz__answers", queryset=AnswersQuiz.objects.all(), to_attr="all_answers"))
            .order_by("-id")
        )

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет статистику ответов в контекст."""
        context = super().get_context_data(**kwargs)

        total_answers = self.get_queryset().count()
        correct_answers = self.get_queryset().filter(current_status=True).count()

        if total_answers > 0:
            success_rate = round((correct_answers / total_answers) * 100, 2)
        else:
            success_rate = 0

        unique_users = TelegramUser.objects.filter(pollusersending__quiz_user=self.request.user).distinct().count()

        context.update(
            {
                "total_answers": total_answers,
                "correct_answers": correct_answers,
                "success_rate": success_rate,
                "unique_users": unique_users,
            }
        )

        return context
