from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import UUIDModel, TimeStampedModel, StatusField


# Create your models here.


class Payment(UUIDModel, TimeStampedModel):
    order = models.ForeignKey("marketplace.Order", verbose_name=_("Commande"), on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(_("Montant"))


class ProviderRefund(UUIDModel, TimeStampedModel, StatusField):
    STATUS = Choices("pending", "processing", "completed")
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("Fournisseur"), on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("marketplace.Order", verbose_name=_("Commande"), on_delete=models.SET_NULL, null=True)
    order_item = models.ForeignKey("marketplace.OrderItem", verbose_name=_("Commande"), on_delete=models.PROTECT)
    amount = models.FloatField(_("Montant"), editable=False)


    def request_refund(self):
        self.status = "processing" if self.status == "pending" else self.status
        self.save()
    
    def save(self, *args, **kwargs):
        self.amount = self.order_item.total
        super().save()