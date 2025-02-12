from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cartapp.models import Cart, CartProduct
from cartapp.views import create_cart
from orderapp.models import Order, OrderDetail
from productsapp.models import Product


# Create your views here.
@login_required(login_url="login")
def order(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")

            try:
                cart = Cart.objects.get(
                    cart_id=create_cart(request), customer=request.user
                )
            except Cart.DoesNotExist:
                return redirect("index")

            cartProduct = CartProduct.objects.filter(cart=cart)
            if not cartProduct.exists():
                return render(request, "cart.html")

            total = 0
            for product in cartProduct:
                total += product.product.price * product.quantity

            order = Order.objects.create(
                fullname=name,
                phone=phone,
                address=address,
                total=total,
                customer=request.user,
            )
            order.save()

            for product in cartProduct:
                orderDetail = OrderDetail.objects.create(
                    product=product.product.name,
                    price=product.product.price,
                    quantity=product.quantity,
                    order=order,
                )
                orderDetail.save()

                productItem = Product.objects.get(pk=product.product.id)
                productItem.stock = int(product.product.stock - orderDetail.quantity)
                productItem.save()
                product.delete()
            cart.delete()

            return render(request, "order_success.html")
        except Exception as e:
            return redirect("index")
    else:
        try:
            cart = Cart.objects.get(cart_id=create_cart(request), customer=request.user)
            cartProduct = CartProduct.objects.filter(cart=cart)
            if not cartProduct.exists():
                return redirect("index")

            return render(request, "order.html")
        except Cart.DoesNotExist:
            return redirect("index")


@login_required(login_url="login")
def order_history(request):
    orders = Order.objects.filter(customer=request.user)
    page = request.GET.get("page", 1)
    paginator = Paginator(orders, 5)
    orders = paginator.get_page(page)
    page_range = calculate_page_range(orders)
    return render(
        request, "order_history.html", {"orders": orders, "page_range": page_range}
    )


def calculate_page_range(page_object):
    paginator = page_object.paginator
    current_page = page_object.number
    total_pages = paginator.num_pages

    if total_pages <= 5:
        return range(1, total_pages + 1)

    pages = []
    start_page = current_page - 2
    end_page = current_page + 2

    if start_page <= 0:
        start_page = 1
        end_page = 5

    if end_page > total_pages:
        start_page = total_pages - 4
        end_page = total_pages

    for page in range(start_page, end_page + 1):
        pages.append(page)

    return pages


@login_required(login_url="login")
def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.customer == request.user:
        orderItems = OrderDetail.objects.filter(order=order)
        return render(
            request, "order_detail.html", {"order_items": orderItems, "order": order}
        )
    else:
        return redirect("order_history")
