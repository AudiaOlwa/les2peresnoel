# Generated by Django 4.1.5 on 2024-07-21 11:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0003_journalentry_amount"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="depth",
        ),
        migrations.RemoveField(
            model_name="account",
            name="numchild",
        ),
        migrations.RemoveField(
            model_name="account",
            name="path",
        ),
    ]
