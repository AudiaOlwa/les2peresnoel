import sweetify
from django.conf import settings
from django.views import View
from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.http import require_POST
from paypal.standard.forms import PayPalPaymentsForm
from les2peresnoel.marketplace.models import Order


from .models import ProviderRefund

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
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payments:paypal_return')),
        "cancel_return": request.build_absolute_uri(reverse('payments:paypal_cancel')),
        # Custom command to correlate to some function later (optional)
        # "custom": "premium_plan",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    _context = {"form": form, "order": order}
    return render(request, "payments/partials/paypal/checkout.html", _context)


def paypal_return(request):
    # sweetify.toast(request, _("Paiement  !"))
    return redirect(reverse('marketplace:home'))
    # return render(request, "payments/paypal/return.html")


def paypal_cancel(request):
    sweetify.toast(request, _("Paiement annulé !"))
    return redirect(reverse('marketplace:home'))
    # return render(request, "payments/paypal/cancel.html")


def credit_card(request):
    _context = {}
    if request.method == "POST":
        ...
        # Process credit card request here
        # We must use a credit card provider
    return render_block("payments/pay_order.html", "init_payment", _context)


@require_POST
def refunder(request, pk):
    """
        We want to pay the provider for the product our client bought

        This case is for one product
    """

    _refund = get_object_or_404(ProviderRefund, pk=pk)
        
    if "completed" ==  _refund.status:
        sweetify.toast(request, _("Cette requête a déjà été traitée"))
    else:
        _refund.request_refund()
        # process the payment via PAYPAL
        ...

    sweetify.toast(request, _("Opération traitée avec succès !"))
    return_url = request.POST.get("return_url") or reverse('marketplace:dashboard')
    return redirect(return_url)


@require_POST
def bulk_refunder(request):
    """
        We want to pay the provider for the product our client bought

        This case is for one product
    """
    
    _refunds = ProviderRefund.objects.filter(provider=request.user).exclude(status="completed")
    total_amount = _refunds.aggregate(Sum('amount')).get('amount__sum') or 0.0
    # Process the payment now

    # We assume that payment processing is successfully
    for r in _refunds:
        r.status = "completed"

    ProviderRefund.bulk_update(_refunds, ['status'])

    sweetify.toast(request, _("Opération traitée avec succès !"))
    return_url = request.POST.get(
        "return_url") or reverse('marketplace:dashboard')
    return redirect(return_url)
