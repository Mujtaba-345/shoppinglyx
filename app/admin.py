from django.contrib import admin
from .models import (
    Customer,
    Product,
    OrderPlaced,
    Cart,
    Category,
    State,
    ProductComment,
    Brand,
    City
)

from django.utils.html import format_html
from django.urls import reverse


# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name']


@admin.register(State)
class StateModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'state']

@admin.register(City)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'city']
@admin.register(ProductComment)
class ProductCommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'user', 'product', 'parent']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category',
                    'product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity', 'ordered_date',
                    'status']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
