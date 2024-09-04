# Generated by Django 4.2.14 on 2024-09-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0010_order_customer_order_tracking_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="media",
            field=models.FileField(
                blank=True, null=True, upload_to="products/media/", verbose_name="Média"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="products/", verbose_name="Couverture"),
        ),
    ]
