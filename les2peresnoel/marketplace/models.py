from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

from .managers import SoftDeletableManager
from .models_abstract import Detail


# Create your models here.
class Category(Detail, TimeStampedModel, SoftDeletableModel):
    slug = models.SlugField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    soft_objects = SoftDeletableManager()

    def __str__(self):
        return self.name


class Product(Detail, TimeStampedModel, SoftDeletableModel):
    slug = models.SlugField(max_length=100)
    price = models.FloatField(verbose_name=_("Prix"))
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name=_("Catégorie")
    )
    quantity = models.IntegerField(verbose_name=_("Quantité"))
    external_link = models.URLField(help_text=_("Lien de drop shipping"))

    def __str__(self):
        return f"{self.name}-{self.category.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    external_link = models.URLField(help_text=_("Lien externe"))
    is_cover = models.BooleanField(default=False)

    @property
    def get_url(self):
        return self.image.url or self.external_link

    def __str__(self):
        return self.product.name
