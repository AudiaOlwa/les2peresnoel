from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Command(BaseCommand):
    help = _('Loads the default configuration')

    def handle(self, *args, **options):
        try:
            from ...models import ChartOfAccount
            from ...helpers import import_accounts_from_excel
            coa, created = ChartOfAccount.objects.get_or_create(name="default", description=_("Plan comptable par défaut"))
            import_accounts_from_excel(settings.APPS_DIR / "accounting" / "default.xlsx", coa=coa)
            # Todo :: Configuration from import file path rather be in settings
        except Exception as e:
            raise e
