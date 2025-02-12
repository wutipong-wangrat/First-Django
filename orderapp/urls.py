from django.urls import path
from orderapp import views

urlpatterns = [
    path("orderHistory", views.order_history, name="orderHistory"),
    path("order/<int:order_id>", views.order_detail, name="order"),
    path("order", views.order, name="order"),
]
