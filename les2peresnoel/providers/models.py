from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class Provider(UUIDModel, TimeStampedModel):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    licence_key = models.CharField(max_length=36, unique=True, editable=False)
    company_name = models.CharField(_("Nom de l'entreprise"), max_length=200)
    company_address = models.TextField(
        _("Adresse de l'entreprise"), help_text=_("Adresse complète de l'entreprise"))
    company_phone = models.CharField(_("Téléphone de l'entreprise"), max_length=20, help_text=_(
        "Numéro de téléphone de l'entreprise"))
    company_email = models.EmailField(
        _("Email de l'entreprise"), help_text=_("Email de l'entreprise"))
    company_website = models.URLField(
        _("Site web de l'entreprise"), blank=True, help_text=_("Site web de l'entreprise"))
    company_logo = models.ImageField(
        _("Logo de l'entreprise"), upload_to="company_logos")
    company_country = CountryField()
    company_id_number = models.CharField(max_length=20, verbose_name=_(
        "Numéro d'identification fiscale"), help_text=_("Numéro d'identification fiscale de l'entreprise"))
    company_description = models.TextField(
        _("Description de l'entreprise"), blank=True, help_text=_("Description de l'entreprise"))

    def __str__(self):
        return self.company_name

    @property
    def has_active_licence(self):
        return self.licence_set.filter(is_active=True).exists()
    
