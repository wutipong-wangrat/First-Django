from django.urls import path
from cartapp import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("cart/add/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/remove/<int:product_id>", views.remove_from_cart, name="remove_from_cart"
    ),
]
