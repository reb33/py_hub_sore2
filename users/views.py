from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            session_key = request.session.session_key
            if user:
                auth.login(request, user)
                messages.success(request, f"Вход {username}")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                if redirect_page := request.POST.get("next", None):
                    if redirect_page != reverse("user:logout"):
                        return HttpResponseRedirect(redirect_page)
                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()
    context = {
        "title": "Home - Авторизация",
        "form": form,
    }
    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"Создание и вход {user.username}")
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Home - Регистрация",
        "form": form,
    }
    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST,
            instance=request.user,  # передаем авторизованного пользователя
            files=request.FILES,  # для сохранения файлов
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = ProfileForm(instance=request.user)  # передаем авторизованного пользователя

    context = {
        "title": "Home - Кабинет",
        "form": form,
    }
    return render(request, "users/profile.html", context)


def user_carts(request):
    return render(request, "users/user_carts.html")


@login_required
def logout(request):
    messages.success(request, f"Выход {request.user.username}")
    auth.logout(request)
    return redirect(reverse("main:index"))
