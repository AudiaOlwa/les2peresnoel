from django.contrib import admin
from unfold.admin import ModelAdmin

from config.sites import manager_admin_site

from .models import Category, Checkout, Order, OrderItem, Product, ProductImage

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Checkout)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Order, site=manager_admin_site)
class OrderAdmin(ModelAdmin):
    pass


@admin.register(OrderItem, site=manager_admin_site)
class OrderItemAdmin(ModelAdmin):
    pass


@admin.register(Checkout, site=manager_admin_site)
class CheckoutAdmin(ModelAdmin):
    pass


@admin.register(Category, site=manager_admin_site)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "description", "parent")


@admin.register(Product, site=manager_admin_site)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "description", "price")

    def save_model(self, request, obj, form, change):
        if not change or not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductImage, site=manager_admin_site)
class ProductImageAdmin(ModelAdmin):
    pass
