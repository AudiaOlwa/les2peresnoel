from django.urls import path

from . import views

app_name = "stores"

urlpatterns = [
    path("products", views.product_list, name="product_list"),
    path("products/create", views.product_create, name="product_create"),
    path("products/<pk>/details", views.OnProductDetailsView.as_view(), name="product_details"),
    path("products/<pk>/update", views.OnProductEditView.as_view(), name="product_edit"),
    path("products/<pk>/delete", views.OnProductDeleteView.as_view(), name="product_delete"),
    path("products/<pk>/add", views.OnProductAddView.as_view(), name="product_add"),
]
