from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = "Create Superuser Automatically"

    def handle(self, *args, **kwargs):

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")

        email = os.environ.get(
            "DJANGO_SUPERUSER_EMAIL",
            "admin@example.com"
        )

        password = os.environ.get(
            "DJANGO_SUPERUSER_PASSWORD",
            "admin12345"
        )

        if not User.objects.filter(username=username).exists():

            User.objects.create_superuser(

                username=username,

                email=email,

                password=password

            )

            self.stdout.write(

                self.style.SUCCESS(

                    "Superuser Created Successfully."

                )

            )

        else:

            self.stdout.write(

                self.style.WARNING(

                    "Superuser Already Exists."

                )

            )