import sweetify
from django.db import transaction
from django.dispatch import receiver, Signal
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.conf import settings
from .models import Payment
from ..accounting.models import Account, Transaction, JournalEntry
from ..core.views import notify_user
from django.utils.translation import gettext_lazy as _
from ..marketplace.models import Order


from ..accounting.helpers import process_accounting_for_customer_order, process_payment_accounting, process_commissions_accounting, process_supplier_accounting

fake_ipn_received = Signal()

live_ipn_received = Signal()


class SimulationResponse:
    receiver_email = settings.PAYPAL_RECEIVER_EMAIL
    payment_status = ST_PP_COMPLETED

    def __init__(self, invoice, mc_gross, mc_currency):
        self.invoice = invoice
        self.mc_gross = mc_gross
        self.mc_currency = mc_currency


# @receiver(valid_ipn_received)
@receiver(fake_ipn_received)
def paypal_call_back_handler(sender, **kwargs):
    # breakpoint()
    ipn_response = sender
    order = Order.objects.get(pk=ipn_response.invoice)
    # customer = payment_request.customer
    if ipn_response.payment_status == ST_PP_COMPLETED:
        if ipn_response.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            # Warn  the user about this, but stop the rest of the code

            # Todo :: 1) Send an email to the user
            notify_user(customer, "Paiement invalide", _(
                "Un problème à malheureusement été détecté. Votre paiement n'as pas pu être validé. Veuillez patienter pendant que nous effectuons des vérifications."))
            # Todo :: 2) Send a notification on the user interface
            # Todo :: 3) Report the incidence to the fraud  service
            ...
        else:
            # Valid payment

            if ipn_response.mc_gross > 0 and ipn_response.mc_currency == payment_request.quotation.currency.code:
                with transaction.atomic():
                    checkout = order.checkout
                    checkout.payment_method = "paypal"
                    # Todo :: Notify user after payment callback
                    # notify_user(customer, "Paiement accepté",
                    #             _("Paiement de %s %s accepté avec succès" % (
                    #                 ipn_response.mc_gross, ipn_response.mc_currency)), )
                    _payment, _created = Payment.objects.get_or_create(order=order, amount=ipn_response.mc_gross)
                    # Todo :: Accountant entries must be done next

                    #  Processing accounting for order registration
                    process_accounting_for_customer_order(
                        payment.amount, description="Commande : " % order.pk)

                    # Processing accounting for payment
                    process_payment_accounting(
                        payment.amount, description="Paiement : " % order.pk)
                    