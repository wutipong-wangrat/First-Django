from django.shortcuts import render, redirect
from productsapp.models import Product
from cartapp.models import Cart, CartProduct
from django.contrib.auth.decorators import login_required
from django.db import transaction, connection


# Create your views here.
def create_cart(request):
    cart_id = request.session.get("cart_id")
    if not cart_id:
        if request.user.is_authenticated:
            cart = Cart.objects.create(customer=request.user)
        else:
            cart = Cart.objects.create(customer=None)
        request.session["cart_id"] = cart.id
        return cart.id
    return cart_id


@login_required(login_url="login")
def cart(request):
    counter = 0
    total = 0

    try:
        cart = Cart.objects.get(cart_id=create_cart(request), customer=request.user)
        cartProducts = CartProduct.objects.filter(cart=cart)
        for product in cartProducts:
            counter += product.quantity
            total += product.quantity * product.product.price
    except (Cart.DoesNotExist, CartProduct.DoesNotExist):
        cart = None
        cartProducts = None

    return render(
        request,
        "cart.html",
        {
            "cartProducts": cartProducts,
            "counter": counter,
            "total": total,
        },
    )


@login_required(login_url="login")
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    try:
        cart = Cart.objects.get(cart_id=create_cart(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=create_cart(request), customer=request.user)
        cart.save()

    try:
        cartProduct = CartProduct.objects.get(product=product, cart=cart)
        if cartProduct.quantity < cartProduct.product.stock:
            cartProduct.quantity += 1
            cartProduct.save()
    except CartProduct.DoesNotExist:
        cartProduct = CartProduct.objects.create(product=product, cart=cart, quantity=1)
        cartProduct.save()
    print(product)

    return redirect("cart")


@login_required(login_url="login")
def remove_from_cart(request, product_id):
    try:
        with transaction.atomic():
            cart = Cart.objects.get(cart_id=create_cart(request), customer=request.user)
            product = Product.objects.get(pk=product_id)
            cartProduct = CartProduct.objects.get(product=product, cart=cart)
            cartProduct.delete()

            if not CartProduct.objects.filter(cart=cart).exists():
                cart.delete()

        return redirect("cart")
    except:
        return redirect("cart")
