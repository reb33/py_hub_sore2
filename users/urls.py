from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("profile/", views.profile, name="profile"),
    path("user-carts/", views.user_carts, name="user_carts"),
    path("logout/", views.logout, name="logout"),
]
