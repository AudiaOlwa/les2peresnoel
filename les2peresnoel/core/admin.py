from django.contrib import admin
from unfold.admin import ModelAdmin

from config.sites import manager_admin_site
from les2peresnoel.core.models import Contact

# # Register your models here.
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("nom", "file", "type", "age", "cover_image")


# admin.site.register(Product, ProductAdmin)


# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ("title",)


# admin.site.register(Document, DocumentAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")


admin.site.register(Contact, ContactAdmin)


@admin.register(Contact, site=manager_admin_site)
class ContactAdmin(ModelAdmin):
    list_display = ("name", "email", "message")
