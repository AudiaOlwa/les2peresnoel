from django.contrib import admin

from .models import Category, Product, ProductImage, Order, OrderItem, Checkout

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Checkout)
admin.site.register(Order)
admin.site.register(OrderItem)