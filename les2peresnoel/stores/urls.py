from django.urls import path

from . import views

app_name = "stores"

urlpatterns = [
    path("products", views.product_list, name="product_list"),
    path("products/create", views.product_create, name="product_create"),
    path("products/<pk>/details", views.product_details, name="product_details"),
    path("products/<pk>/update", views.product_update, name="product_update"),
    path("products/<pk>/delete", views.product_delete, name="product_delete"),
]
