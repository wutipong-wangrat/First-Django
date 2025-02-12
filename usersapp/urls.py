from django.urls import path
from usersapp import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.regiseter, name="register"),
    path("logout", views.logout, name="logout"),
]
