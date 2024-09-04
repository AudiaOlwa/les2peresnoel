import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, StatusModel, UUIDModel
from django_countries.fields import CountryField
from model_utils import Choices
from django.urls import reverse
User = get_user_model()
from django.utils import timezone

# Create your models here.

class LicenceRequest(TimeStampedModel, StatusModel, UUIDModel):
    STATUS = Choices("pending", "approved", "rejected")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="licence_requests")
    licence_key = models.CharField(max_length=36, unique=True)
    company_name = models.CharField(_("Nom de l'entreprise"), max_length=200)
    company_address = models.TextField(_("Adresse de l'entreprise"), help_text=_("Adresse complète de l'entreprise"))
    company_phone = models.CharField(_("Téléphone de l'entreprise"), max_length=20, help_text=_("Numéro de téléphone de l'entreprise"))
    company_email = models.EmailField(_("Email de l'entreprise"), help_text=_("Email de l'entreprise"))
    company_website = models.URLField(_("Site web de l'entreprise"), blank=True, help_text=_("Site web de l'entreprise"))
    company_logo = models.ImageField(_("Logo de l'entreprise"), upload_to="company_logos")
    company_country = CountryField()
    company_id_number = models.CharField(max_length=20, verbose_name=_("Numéro d'identification fiscale"), help_text=_("Numéro d'identification fiscale de l'entreprise"))
    company_description = models.TextField(
        _("Description de l'entreprise"), blank=True, help_text=_("Description de l'entreprise"))
    message = models.TextField(_("Message"), blank=True, help_text=_("Message à l'attention de MPERESBONHEUR"))


    def __str__(self):
        return f"{self.user.username} - {self.licence_key}"
    
    @property
    def generate_licence_key(self):
        return str(uuid.uuid4())
    
    def accept(self):
        self.status = self.STATUS.approved
        self.save()
    
    def reject(self):
        self.status = self.STATUS.rejected
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.licence_key:
            self.licence_key = self.generate_licence_key
        super().save(*args, **kwargs)

class LicenceRequestAttachment(TimeStampedModel, UUIDModel):
    licence_request = models.ForeignKey(LicenceRequest, on_delete=models.CASCADE)
    attachment = models.FileField(_("Pièce jointe"), upload_to="licence_request_attachments")
    name = models.CharField(_("Nom"), max_length=200, help_text=_("Nom de la pièce jointe"))
    description = models.TextField(_("Description"), blank=True, help_text=_("Description de l'attachement"))

    def __str__(self):
        return f"{self.licence_request.user.username} - {self.licence_request.licence_key}"


class Licence(TimeStampedModel, UUIDModel):
    licence_key = models.CharField(max_length=36, unique=True)
    provider = models.ForeignKey("providers.Provider", on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="licences")
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(_("Date d'expiration"), null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_licences")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_licences")

    def __str__(self):
        return f"{self.licence_key}"
    
    @property
    def is_expired(self):
        return self.expires_at < timezone.now()
    
    def update_status(self):
        if self.is_expired:
            self.is_active = False
        else:
            self.is_active = not self.is_active
        self.save()
    
    @property
    def get_update_url(self):
        return reverse("licences:licence_update", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.owner:
            self.owner = self.provider.owner
        super().save(*args, **kwargs)
