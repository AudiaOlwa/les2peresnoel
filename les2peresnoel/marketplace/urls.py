from django.urls import path, re_path

from . import views

app_name = "marketplace"

urlpatterns = [
    # Products
    path("", views.home, name="home"),
    path("products", views.list_product, name="products"),
    path("products/create", views.create_product, name="create_product"),
    path("products/<int:pk>/update", views.update_product, name="update_product"),
    path("products/<int:pk>/delete", views.delete_product, name="delete_product"),
    path("products/<int:pk>/detail", views.detail_product, name="detail_product"),
    # Categories
    path("categories", views.list_category, name="categories"),
    path("categories/create", views.create_category, name="create_category"),
    path("categories/<int:pk>/update", views.update_category, name="update_category"),
    path("categories/<int:pk>/delete", views.delete_category, name="delete_category"),
    path("categories/<int:pk>/detail", views.detail_category, name="detail_category"),
]
