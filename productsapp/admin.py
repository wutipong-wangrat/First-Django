from django.contrib import admin
from productsapp.models import Product


class ManageProduct(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "isTrending"]
    list_editable = ["price", "stock", "isTrending"]
    list_per_page = 5
    list_filter = ["isTrending"]
    ordering = ["name"]
    search_fields = ["name"]
    search_help_text = "Search by name"


# Register your models here.
admin.site.register(Product, ManageProduct)
