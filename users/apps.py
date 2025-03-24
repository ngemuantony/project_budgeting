from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "users"
    verbose_name = _("Users")

    def ready(self):
        """Import signals when the app is ready."""
        try:
            import users.signals  # noqa F401
            print("UsersConfig ready - signals imported")
        except ImportError:
            print("Error importing users signals")
