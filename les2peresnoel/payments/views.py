import sweetify
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import View
from django.views.decorators.http import require_POST
from paypal.standard.forms import PayPalPaymentsForm

from ..marketplace.models import Order
from ..payments.models import Payment
from .models import ProviderRefund
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRedirect

from django.utils.translation import gettext_lazy as _
# Create your views here.


def pay_order_tracked(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    return render(request, "payments/pay_order.html", {"order": order})


def pay_with_paypal(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "currency_code": "EUR",
        "amount": "{:.2f}".format(order.total_ttc),
        # "item_name": "name of the item",
        "invoice": "{}".format(order.pk),
        "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
        "return": request.build_absolute_uri(reverse("payments:paypal_return")),
        "cancel_return": request.build_absolute_uri(reverse("payments:paypal_cancel")),
        # Custom command to correlate to some function later (optional)
        # "custom": "premium_plan",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    _context = {"form": form, "order": order}
    return render(request, "payments/partials/paypal/checkout.html", _context)


def paypal_return(request):
    # sweetify.toast(request, _("Paiement  !"))
    return redirect(reverse("marketplace:home"))
    # return render(request, "payments/paypal/return.html")


def paypal_cancel(request):
    sweetify.toast(request, _("Paiement annulé !"))
    return redirect(reverse("marketplace:home"))
    # return render(request, "payments/paypal/cancel.html")

@login_required
def credit_card(request, order_pk):
    # breakpoint()
    _order = get_object_or_404(Order, pk=order_pk)
    _context = {
        "order": _order
    }
    
    stripe.api_key = 'sk_test_51Hzfd8JbhXB8bKJseVqt2FN0JLrbAMw5HVxBhhPnE0Ieu4mavy8wriMDbfOkS0p6nvLCAxDvR02IfdIiEJFJHLkD00SY1hVWz1'
    if request.method == "POST":
        print([item.price for item in _order.items.all()])
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': item.product.name,
                            },
                            'unit_amount': int(round(item.price * 100)),
                        },
                        'quantity': item.quantity,
                    }
                    for item in _order.items.all()
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse("payments:credit_card_success", kwargs={"order_pk": _order.pk})),
                cancel_url=request.build_absolute_uri(reverse("payments:credit_card_cancel")) ,
                client_reference_id=str(_order.pk),
                customer_email=request.user.email,
            )
        except Exception as e:
            print(e.__str__())
            return HttpResponse(str(e), status=400)
        return HttpResponseClientRedirect(checkout_session.url)
    return render(request, "payments/pay_order.html", _context)


def credit_card_success(request, order_pk):
    _order = get_object_or_404(Order, pk=order_pk)
    Payment.objects.create(order=_order, amount=_order.total_ttc, payer=request.user)
    sweetify.success(request, _("Paiement réussi !"))
    return redirect(reverse("marketplace:home"))
    # return render(request, "payments/credit_card/success.html")


def credit_card_cancel(request):
    sweetify.warning(request, _("Paiement annulé !"))
    return redirect(reverse("marketplace:home"))
    # return render(request, "payments/credit_card/cancel.html")


@require_POST
def refunder(request, pk):
    """
    We want to pay the provider for the product our client bought

    This case is for one product
    """

    _refund = get_object_or_404(ProviderRefund, pk=pk)

    if "completed" == _refund.status:
        sweetify.toast(request, _("Cette requête a déjà été traitée"))
    else:
        _refund.request_refund()
        # process the payment via PAYPAL
        ...

    sweetify.toast(request, _("Opération traitée avec succès !"))
    return_url = request.POST.get("return_url") or reverse("marketplace:dashboard")
    return redirect(return_url)


@require_POST
def bulk_refunder(request):
    """
    We want to pay the provider for the product our client bought

    This case is for one product
    """

    _refunds = ProviderRefund.objects.filter(provider=request.user).exclude(
        status="completed"
    )
    total_amount = _refunds.aggregate(Sum("amount")).get("amount__sum") or 0.0
    # Process the payment now

    # We assume that payment processing is successfully
    for r in _refunds:
        r.status = "completed"

    ProviderRefund.bulk_update(_refunds, ["status"])

    sweetify.toast(request, _("Opération traitée avec succès !"))
    return_url = request.POST.get("return_url") or reverse("marketplace:dashboard")
    return redirect(return_url)


def list_payments(request):
    _payments = Payment.objects.all()
    return render(request, "payments/list.html", {"payments": _payments})
