from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ..providers.models import Provider

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Belle sans leurre.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
    
    @property
    def is_provider(self):
        try:
            Provider.objects.get(account=self)
            return True
        except:
            pass
        return False

    @property
    def is_active_provider(self):
        try:
            provider = Provider.objects.get(account=self)
            return provider.has_active_licence
        except:
            return False

    @property
    def can_manage_stock(self):
        return self.is_active_provider or self.is_superuser or self.is_staff