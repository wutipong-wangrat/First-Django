from django.db import models, connection
from django.contrib.auth.models import User
from productsapp.models import Product
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True
    )

    def __str__(self):
        return self.cart_id


@receiver(post_delete, sender=Cart)
def reset_auto_increment(sender, instance, **kwargs):
    if not Cart.objects.exists():
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE cartapp_cart AUTO_INCREMENT = 1")


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name + " " + str(self.quantity)
