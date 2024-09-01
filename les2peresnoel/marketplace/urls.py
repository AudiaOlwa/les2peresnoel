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
    # DASHBOARD
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "add_to_cart/<product_id>", views.add_product, name="add_to_cart"
    ),
    path(
        "update_cart_count", 
        views.update_cart_count, 
        name="update_cart_count"
    ),
    path(
        "update_cart", 
        views.update_cart, 
        name="update_cart"
    ),
    path(
        "remove_product",
        views.remove_product, 
        name="remove_product"
    ),

    # Checkout

    path(
        "checkout/",
        views.CheckoutView.as_view(),
        name="checkout"
    ),
    path(
        "update_checkout",
        views.update_checkout,
        name="update_checkout"
    ),
    # Orders
    path(
        'orders',
        views.order_list,
        name="order_list"
    ),
    path(
        'orders/<pk>',
        views.order_details,
        name="order_detail"
    ),
    path(
        'orders/<tracking_id>/tracking',
        views.order_tracking,
        name="order_tracking"
    ),

    path(
        'categories/<int:pk>/products', 
        views.list_product_by_category, 
        name='list_product_by_category'
    ),
]
