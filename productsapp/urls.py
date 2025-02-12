from django.urls import path
from productsapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("product/detail/<int:product_id>", views.productDetail, name="productDetail"),
]
