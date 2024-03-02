from django.db import models
from django.utils.translation import gettext_lazy as _


class Detail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    class Meta:
        abstract = True
