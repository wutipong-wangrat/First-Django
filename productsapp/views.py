from django.shortcuts import render
from django.http import HttpResponse
from productsapp.models import Product
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    products = Product.objects.filter(isTrending=True)
    return render(request, "index.html", {"products": products})


def products(request):
    products = Product.objects.all().order_by("name")
    page = request.GET.get("page", 1)
    paginator = Paginator(products, 3)
    products = paginator.get_page(page)
    page_range = calculate_page_range(products)

    return render(
        request, "products.html", {"products": products, "page_range": page_range}
    )


def calculate_page_range(page_object):
    paginator = page_object.paginator
    current_page = page_object.number
    total_pages = paginator.num_pages

    if total_pages <= 5:
        return range(1, total_pages + 1)

    pages = []

    pages.append(1)

    start_range = max(2, current_page - 1)
    end_range = min(total_pages - 1, current_page + 1)
    print(start_range, end_range, total_pages)

    if start_range > 2:
        pages.append(None)

    pages.extend(range(start_range, end_range + 1))

    if end_range < total_pages - 1:
        pages.append(None)

    if total_pages not in pages:
        pages.append(total_pages)

    return pages


def productDetail(request, product_id):
    products = Product.objects.filter(id=product_id)
    return render(request, "detail.html", {"products": products})
