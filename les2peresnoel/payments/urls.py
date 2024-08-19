from django.urls import path

from .views import pay_order_tracked, paypal_return, paypal_cancel, pay_with_paypal, credit_card, refunder, bulk_refunder

app_name = "payments"

urlpatterns = [
    path(
        'pay_tracked_order/<order_pk>/',
        pay_order_tracked,
        name='pay_tracked_order'
    ),
    path(
        "credit_card",
        credit_card,
        name="credit_card"
    ),
    path(
        'paypal/<order_pk>',
        pay_with_paypal,
        name="paypal"
    ),
    path(
        'paypal_return',
        paypal_return,
        name='paypal_return'
    ),
    path(
        'paypal_cancel',
        paypal_cancel,
        name='paypal_cancel'
    ),
    path(
        'refunder',
        refunder,
        name='refunder'
    ),
    path(
        'refunder/bulk',
        bulk_refunder,
        name="bulk_refunder"
    )
]
