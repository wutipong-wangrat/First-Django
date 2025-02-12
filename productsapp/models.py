from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    isTrending = models.BooleanField(default=False)
    image = ProcessedImageField(
        upload_to="products",
        processors=[ResizeToFill(650, 500)],
        format="WEBP",
        options={"quality": 85},
        blank=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
