import random
import string

from dj_shop_cart.cart import CartItem
from dj_shop_cart.protocols import Numeric
from django import forms
from django.conf import settings
from django.db import models
from django.db.models import (BooleanField, Case, Exists, OuterRef, Q, Value,
                              When)
from django.db.models.functions import Coalesce
from django.db.transaction import atomic as atomic_transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import (SoftDeletableModel, StatusModel,
                                TimeStampedModel, UUIDModel)

from les2peresnoel.utils import generate_unique_slug

from ..payments.models import ProviderRefund
from ..users.models import User
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
    quantity = models.IntegerField(verbose_name=_("Quantité"), default=1)
    external_link = models.URLField(help_text=_("Lien de dropshipping"), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(upload_to="products/", verbose_name=_("Couverture"))
    media = models.FileField(
        upload_to="products/media/", verbose_name=_("Média"), blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}-{self.category.name}"

    @classmethod
    def get_available(cls):
        from ..licences.models import \
            Licence  # Import local pour éviter les imports circulaires

        active_licence = Licence.objects.filter(
            provider=OuterRef("owner__providers"), is_active=True
        )

        return (
            cls.objects.select_related("owner")
            .annotate(
                owner_can_manage_stock=Case(
                    When(owner__is_superuser=True, then=Value(True)),
                    When(owner__is_staff=True, then=Value(True)),
                    When(Exists(active_licence), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .filter(owner_can_manage_stock=True)
        )

    def get_price(self, item: CartItem) -> Numeric:
        return float(self.price)

    @property
    def is_available(self):
        return self.owner.can_manage_stock

    @property
    def media_url(self):
        return self.media.url if self.media else None

    @property
    def can_be_sold(self):
        # check if the product product.owner is a provider and has a licence
        return self.owner.profile.is_provider and self.owner.profile.licence.is_active

    def is_available_for_quantity(self, quantity):
        return self.quantity > quantity

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


class Checkout(UUIDModel, TimeStampedModel):
    last_name = models.CharField(max_length=50, verbose_name=_("Nom"))
    first_name = models.CharField(max_length=50, verbose_name=_("Prénom(s)"))
    address = models.CharField(max_length=100, verbose_name=_("Adresse"))
    city = models.CharField(max_length=100, verbose_name=_("Ville"))
    zip_code = models.CharField(max_length=20, verbose_name=_("Code Postal"))
    country = models.CharField(max_length=50, verbose_name=_("Country"))
    email = models.EmailField(
        max_length=50, blank=True, verbose_name=_("Adresse E-mail")
    )
    phone_number = models.CharField(
        max_length=50, blank=True, verbose_name=_("Numero de téléphone")
    )
    order_notes = models.TextField(blank=True)
    payment_method = models.CharField(
        choices=[
            ("credit_card", "Credit Card"),
            ("paypal", "PayPal"),
            ("cash", "Cash"),
        ],
        verbose_name=_("Méthode de paiement"),
        max_length=12,
    )
    card_number = models.CharField(max_length=16, blank=True)
    card_expiry = models.CharField(max_length=5, blank=True)
    card_cvv = models.CharField(max_length=3, blank=True)
    paypal_address = models.CharField(_("Adresse PayPal"), max_length=50, blank=True)
    # pay_at_shipping = models.BooleanField(_("Paiement à la livraison"), default=False)


class Order(UUIDModel, TimeStampedModel, StatusModel):
    STATUS = Choices("pending", "processing", "completed")

    last_name = models.CharField(_("Nom"), max_length=50, blank=True)
    first_name = models.CharField(_("Prénoms"), max_length=50, blank=True)
    email = models.EmailField(_("Adresse E-mail"), max_length=254, blank=True)
    total_ht = models.FloatField(_("Total Hors-Taxe"), editable=False)
    total_ttc = models.FloatField(_("Total TTC"), editable=False)
    total_tva = models.FloatField(_("Total TVA"), editable=False)
    shipping_amount = models.FloatField(
        _("Frais de livraison"), editable=False, default=0.0
    )
    checkout = models.ForeignKey(
        "Checkout",
        verbose_name=_("Checkout"),
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
    )
    refund_generated = models.BooleanField(
        _("Redevance générée ?"), default=False, editable=False
    )
    tracking_number = models.CharField(
        _("N° de suivi"), max_length=10, blank=True, editable=False
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Client"),
        on_delete=models.SET_NULL,
        null=True,
    )

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_payment_url(self):
        return reverse("payments:pay_tracked_order", kwargs={"order_pk": self.pk})

    def generate_refund(self):
        with atomic_transaction():
            items = self.orderitem_set.all()
            ProviderRefund.objects.bulk_create(
                [
                    ProviderRefund(order=self, provider=item.provider, order_item=item)
                    for item in items
                ]
            )
            self.refund_generated = True

    @property
    def generate_tracking_number(self):
        # Génère un numéro de suivi de 10 caractères alphanumériques
        tracking_number = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        return tracking_number

    @property
    def grouped_items(self):
        grouped = {}
        for item in self.orderitem_set.all():
            if item.product.id not in grouped:
                grouped[item.product.id] = {
                    "product": item.product,
                    "provider": item.provider,
                    "items": [],
                    "total_quantity": 0,
                    "total_price": 0,
                }
            grouped[item.product.id]["items"].append(item)
            grouped[item.product.id]["total_quantity"] += item.quantity
            grouped[item.product.id]["total_price"] += item.total
        return grouped.values()

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number
        super().save()


class OrderItem(UUIDModel, TimeStampedModel):
    order = models.ForeignKey(
        Order,
        verbose_name=_("Commande"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Fournisseur"),
        on_delete=models.SET_NULL,
        null=True,
    )
    product = models.ForeignKey(
        Product, verbose_name=_("Produit"), on_delete=models.SET_NULL, null=True
    )
    price = models.FloatField(_("Prix"))
    quantity = models.PositiveIntegerField(_("Quantité"), default=1)
    total = models.FloatField(_("Total"), editable=False)

    def save(self, *args, **kwargs):
        self.provider = self.product.owner
        super().save()
