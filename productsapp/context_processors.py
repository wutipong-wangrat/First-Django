from cartapp.models import Cart, CartProduct
from cartapp.views import create_cart


def cart_items(request):
    cartProducts = []
    cartTotal = 0

    try:
        cart_id = create_cart(request)
        cart = Cart.objects.get(cart_id=cart_id)
        cartProducts = CartProduct.objects.filter(cart=cart)
        cartTotal = sum(product.quantity for product in cartProducts)
    except Cart.DoesNotExist:
        pass

    return {"cartProducts": cartProducts, "cartTotal": cartTotal}
