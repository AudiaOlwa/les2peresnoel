from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


# Create your models here.
class Provider(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name
