from dj_shop_cart.cart import CartItem
from dj_shop_cart.protocols import Numeric
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

from les2peresnoel.utils import generate_unique_slug

from .models_abstract import Detail


# Create your models here.
class Category(Detail, TimeStampedModel, SoftDeletableModel):

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    slug = models.SlugField(max_length=100, editable=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    cover_image = models.ImageField(upload_to="categories/", blank=True, null=True)

    @property
    def cover(self):
        return (
            self.cover_image.url
            if self.cover_image
            else settings.MARKETPLACE_DEFAULT.get("category_cover")
        )

    @property
    def items_count(self):
        return self.products.count

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(Category, self.slug, slug_field="slug")
        super().save()


class Product(Detail, TimeStampedModel, SoftDeletableModel):

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")

    slug = models.SlugField(max_length=100, editable=False)
    price = models.FloatField(verbose_name=_("Prix"))
    category = models.ManyToManyField(
        Category, verbose_name=_("Catégorie"), related_name="products"
    )
    # quantity = models.IntegerField(verbose_name=_("Quantité"))
    external_link = models.URLField(help_text=_("Lien de dropshipping"), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.name}-{self.category.name}"

    def get_price(self, item: CartItem) -> Numeric:
        return float(self.price)

    def get_details_for_provider_url(self):
        return reverse("stores:product_details", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("marketplace:detail_product", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(Product, self.slug, slug_field="slug")
        super().save()


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    external_link = models.URLField(help_text=_("Lien externe"))
    is_cover = models.BooleanField(default=False)

    @property
    def get_url(self):
        return self.image.url or self.external_link

    @property
    def get_image(self):
        return self.image.url

    def __str__(self):
        return self.product.name
