from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("payments", views.list_payments, name="list_payments"),
    path(
        "pay_tracked_order/<order_pk>/",
        views.pay_order_tracked,
        name="pay_tracked_order",
    ),
    path("credit_card", views.credit_card, name="credit_card"),
    path("paypal/<order_pk>", views.pay_with_paypal, name="paypal"),
    path("paypal_return", views.paypal_return, name="paypal_return"),
    path("paypal_cancel", views.paypal_cancel, name="paypal_cancel"),
    path("refunder", views.refunder, name="refunder"),
    path("refunder/bulk", views.bulk_refunder, name="bulk_refunder"),
]
