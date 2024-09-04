from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import LicenceRequest

class LicenceRequestForm(ModelForm):
    class Meta:
        model = LicenceRequest
        exclude = ["user", "licence_key", "status", "created", "updated", "id", "status_changed"]
        widgets = {
            "company_logo": forms.FileInput(attrs={"accept": "image/*"}),
            "message": forms.Textarea(attrs={"rows": 3}),
            "company_address": forms.Textarea(attrs={"rows": 3}),
            "company_description": forms.Textarea(attrs={"rows": 3}),
            "company_id_number": forms.TextInput(attrs={"placeholder": "ex: 00000000000000"}),
            # "company_phone": forms.TextInput(attrs={"placeholder": "ex: 06 98 88 88 88"}),
        }


class LicenceRequestAcceptForm(forms.Form):
    expiration_date = forms.DateField(label=_("Date d'expiration"), widget=forms.DateInput(attrs={"type": "date"}))