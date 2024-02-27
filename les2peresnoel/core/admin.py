from django.contrib import admin
from les2peresnoel.core.models import Product, Document


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nom", "file", "type", "age", "cover_image")


admin.site.register(Product, ProductAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Document, DocumentAdmin)
