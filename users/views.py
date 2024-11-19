from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    # success_url = reverse_lazy("main:index")

    def get_success_url(self):
        if redirect_page := self.request.POST.get("next", None):
            if redirect_page != reverse("user:logout"):
                return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Home - Авторизация"
        })
        return context


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"Создание и вход {user.username}")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Регистрация"
        return context


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("user:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлен")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Кабинет"

        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("product")))
            .order_by("-id")
        )

        context["orders"] = self.set_get_cache(orders, f"orders_for_user_{self.request.user.id}", 60)
        return context


class UserCartView(TemplateView):
    template_name = "users/user_carts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Корзина"
        return context


@login_required
def logout(request):
    messages.success(request, f"Выход {request.user.username}")
    auth.logout(request)
    return redirect(reverse("main:index"))


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)
#             session_key = request.session.session_key
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"Вход {username}")
#
#                 if session_key:
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#
#                 if redirect_page := request.POST.get("next", None):
#                     if redirect_page != reverse("user:logout"):
#                         return HttpResponseRedirect(redirect_page)
#                 return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserLoginForm()
#     context = {
#         "title": "Home - Авторизация",
#         "form": form,
#     }
#     return render(request, "users/login.html", context)


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#
#             session_key = request.session.session_key
#
#             user = form.instance
#             auth.login(request, user)
#
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
#
#             messages.success(request, f"Создание и вход {user.username}")
#             return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserRegistrationForm()
#
#     context = {
#         "title": "Home - Регистрация",
#         "form": form,
#     }
#     return render(request, "users/registration.html", context)


# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = ProfileForm(
#             data=request.POST,
#             instance=request.user,  # передаем авторизованного пользователя
#             files=request.FILES,  # для сохранения файлов
#         )
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профиль обновлен")
#             return HttpResponseRedirect(reverse("user:profile"))
#     else:
#         form = ProfileForm(instance=request.user)  # передаем авторизованного пользователя
#
#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("product")))
#         .order_by("-id")
#     )
#     context = {
#         "title": "Home - Кабинет",
#         "form": form,
#         "orders": orders,
#     }
#     return render(request, "users/profile.html", context)


# def user_carts(request):
#     return render(request, "users/user_carts.html")
