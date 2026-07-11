from django.apps import AppConfig
import os
import sys
import logging


logger = logging.getLogger(__name__)


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # Create a superuser automatically at startup when the
        # environment variables are provided and the process is
        # not running a management command like migrate/makemigrations.
        try:
            if os.environ.get("CREATE_SUPERUSER_ON_STARTUP", "False") != "True":
                return

            # Avoid running during migrations or other manage.py commands
            cmd_args = " ".join(sys.argv)
            if any(x in cmd_args for x in ("migrate", "makemigrations", "collectstatic", "createsuperuser")):
                return

            from django.contrib.auth import get_user_model

            User = get_user_model()

            username = os.environ.get("ADMIN_USERNAME")
            email = os.environ.get("ADMIN_EMAIL")
            password = os.environ.get("ADMIN_PASSWORD")

            if not username or not password:
                logger.debug("Admin username/password not provided via env; skipping superuser creation.")
                return

            existing = User.objects.filter(username=username).first()

            # If user exists and ADMIN_FORCE_RESET is set, reset password
            if existing is not None:
                if os.environ.get("ADMIN_FORCE_RESET", "False") == "True":
                    existing.set_password(password)
                    existing.email = email or existing.email
                    existing.save()
                    logger.warning("Reset password for existing superuser '%s' from environment variable.", username)
                else:
                    logger.debug("Superuser '%s' already exists; not creating or resetting.", username)
            else:
                User.objects.create_superuser(username=username, email=email or "", password=password)
                logger.warning("Created superuser '%s' from environment variable.", username)
        except Exception as e:
            # Don't crash the app if something goes wrong here; just log.
            logger.exception("Error while attempting to create superuser on startup: %s", e)
