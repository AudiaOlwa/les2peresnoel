from django import forms
from django.forms import ModelForm

from .models import LicenceRequest

class LicenceRequestForm(ModelForm):
    class Meta:
        model = LicenceRequest
        exclude = ["user", "licence_key", "status", "created", "updated", "id", "status_changed"]
        widgets = {
            "company_logo": forms.FileInput(attrs={"accept": "image/*"}),
            "message": forms.Textarea(attrs={"rows": 3}),
            "company_description": forms.Textarea(attrs={"rows": 3}),
        }