from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "les2peresnoel.payments"

    def ready(self):
        from . import hooks