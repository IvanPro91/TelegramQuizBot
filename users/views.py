from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserProfileForm
from users.models import User


@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect(reverse("marketing:marketing"))


def users_login(request: HttpRequest):
    data_post = request.POST
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        return redirect(reverse("main:main"))

    if data_post:
        email = data_post["email"]
        password = data_post["password"]

        find_user: User | None = User.objects.filter(email=email).first()
        chk_pwd = find_user.check_password(password) if find_user else False

        if not chk_pwd:
            messages.error(request, "Пользователь не прошел проверку по логину или паролю")
            return redirect(reverse("users:login"))

        if chk_pwd and not find_user.is_active:
            return redirect(reverse("users:verification_code"))

        auth.login(request, find_user)
        return redirect(reverse("main:main"))

    return render(request, "login.html")


def users_registration(request: HttpRequest):
    data_post = request.POST
    if data_post:
        first_name: str = data_post["first_name"]
        last_name: str = data_post["last_name"]
        email: str = data_post["email"]
        password: str = data_post["password"]
        repeat_password: str = data_post["repeat_password"]

        if password != repeat_password:
            messages.error(request, "Пароли не совпадают!")
            return redirect(reverse("users:registration"))

        is_new_user, user = User.create_user(first_name, last_name, email, password)
        if is_new_user:
            html_email_template = render_to_string("email/template_email.html", {"code": user.code})
            try:
                send_mail(
                    subject="Подтверждение аккаунта",
                    message="",
                    html_message=html_email_template,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return redirect(reverse("users:verification_code"))
            except Exception as err:
                print(err)
                user.delete()
                messages.error(request, "Произошла непредвиденная ошибка, повторите позже")
                return redirect(reverse("users:registration"))

    return render(request, "registration.html")


def verification_code(request: HttpRequest):
    data_post = request.POST
    if data_post:
        user_code = "".join(list(data_post.dict().values())[1:])
        if user_code:
            user: User = User.objects.filter(code=int(user_code)).first()
            if user:
                user.code = 0
                user.is_active = True
                user.save()

                auth.login(request, user)
                return redirect(reverse("users:login"))

        messages.error(request, "Введите корректный код отправленный на почту!")
        return redirect(reverse("users:verification_code"))

    return render(request, "email/verification_code.html")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    context_object_name = "user"
    template_name = "user/profile.html"
    success_url = reverse_lazy("main:main")
