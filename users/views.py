from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            if user := auth.authenticate(username=username, password=password):
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        "form": form,
    }
    return render(request, 'users/registration.html', context)


def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST,
            instance=request.user,  # передаем авторизованного пользователя
            files=request.FILES,  # для сохранения файлов
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)  # передаем авторизованного пользователя

    context = {
        'title': 'Home - Кабинет',
        "form": form,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse("main:index"))
