# Generated by Django 4.2.14 on 2024-09-03 18:11

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="provider",
            name="company_address",
            field=models.TextField(
                default="",
                help_text="Adresse complète de l'entreprise",
                verbose_name="Adresse de l'entreprise",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_country",
            field=django_countries.fields.CountryField(default="", max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_description",
            field=models.TextField(
                blank=True,
                help_text="Description de l'entreprise",
                verbose_name="Description de l'entreprise",
            ),
        ),
        migrations.AddField(
            model_name="provider",
            name="company_email",
            field=models.EmailField(
                default="",
                help_text="Email de l'entreprise",
                max_length=254,
                verbose_name="Email de l'entreprise",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_id_number",
            field=models.CharField(
                default="",
                help_text="Numéro d'identification fiscale de l'entreprise",
                max_length=20,
                verbose_name="Numéro d'identification fiscale",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_logo",
            field=models.ImageField(
                default="",
                upload_to="company_logos",
                verbose_name="Logo de l'entreprise",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_name",
            field=models.CharField(
                default="", max_length=200, verbose_name="Nom de l'entreprise"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_phone",
            field=models.CharField(
                default="",
                help_text="Numéro de téléphone de l'entreprise",
                max_length=20,
                verbose_name="Téléphone de l'entreprise",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="provider",
            name="company_website",
            field=models.URLField(
                blank=True,
                help_text="Site web de l'entreprise",
                verbose_name="Site web de l'entreprise",
            ),
        ),
        migrations.AddField(
            model_name="provider",
            name="licence_key",
            field=models.CharField(
                default="", editable=False, max_length=36, unique=True
            ),
            preserve_default=False,
        ),
    ]
