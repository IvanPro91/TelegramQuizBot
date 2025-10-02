from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Count, IntegerField, Q, Sum, When
from django.db.models.functions import Coalesce
from django.views.generic import ListView

from telegram_bot.models import TelegramUser


class UserRatingView(LoginRequiredMixin, ListView):
    """Рейтинг пользователей по результатам викторин."""
    template_name = "page_rating.html"
    context_object_name = "user_ratings"
    paginate_by = 50

    def get_queryset(self):
        """Возвращает пользователей с их статистикой ответов."""
        user_ratings = (
            TelegramUser.objects.filter(pollusersending__quiz_user=self.request.user)
            .annotate(
                total_answers=Count("pollusersending"),
                correct_answers=Count("pollusersending", filter=Q(pollusersending__current_status=True)),
                wrong_answers=Count("pollusersending", filter=Q(pollusersending__current_status=False)),
                unique_quizzes=Count("pollusersending__quiz", distinct=True),
                success_rate=Case(
                    When(total_answers=0, then=0),
                    default=100.0
                    * Count("pollusersending", filter=Q(pollusersending__current_status=True))
                    / Count("pollusersending"),
                    output_field=IntegerField(),
                ),
                total_likes=Coalesce(Sum("pollusersending__quiz__feedback_like"), 0),
                total_dislikes=Coalesce(Sum("pollusersending__quiz__feedback_dislike"), 0),
            )
            .filter(total_answers__gt=0)  # Только те, кто хотя бы раз ответил
            .order_by("-correct_answers", "-success_rate", "-total_answers")
        )

        return user_ratings

    def get_context_data(self, **kwargs):
        """Добавляет статистику и топы в контекст."""
        context = super().get_context_data(**kwargs)

        user_ratings = self.get_queryset()

        top_users = user_ratings[:5]

        total_stats = {
            "total_users": user_ratings.count(),
            "total_answers": sum(rating.total_answers for rating in user_ratings),
            "total_correct": sum(rating.correct_answers for rating in user_ratings),
            "avg_success_rate": round(
                sum(rating.success_rate for rating in user_ratings) / (user_ratings.count() or 1), 2
            ),
        }

        most_active = user_ratings.order_by("-total_answers")[:5]

        most_successful = [user for user in user_ratings if user.total_answers >= 5][:5]

        most_diverse = user_ratings.order_by("-unique_quizzes")[:5]

        context.update(
            {
                "total_stats": total_stats,
                "top_users": top_users,
                "most_active": most_active,
                "most_successful": most_successful,
                "most_diverse": most_diverse,
            }
        )

        return context
