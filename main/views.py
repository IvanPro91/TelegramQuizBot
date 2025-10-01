from django.views.generic import ListView

from quiz.models import PollUserSending
from users.models import User


class TelegramUserQuizListView(ListView):
    model = PollUserSending
    template_name = "page_main.html"
    context_object_name = "sending_poll_users"

    def get_queryset(self):
        return User.objects.filter(pollusersending__isnull=False).distinct()
