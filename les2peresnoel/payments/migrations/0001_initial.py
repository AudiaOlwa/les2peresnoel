# Generated by Django 4.2.14 on 2024-08-19 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("marketplace", "0009_order_refund_generated_orderitem_provider_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProviderRefund",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.FloatField(editable=False, verbose_name="Montant")),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="marketplace.order",
                        verbose_name="Commande",
                    ),
                ),
                (
                    "order_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="marketplace.orderitem",
                        verbose_name="Commande",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Fournisseur",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, model_utils.fields.StatusField),
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.FloatField(verbose_name="Montant")),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="marketplace.order",
                        verbose_name="Commande",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
