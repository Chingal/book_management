import os
from django.core.management.base import BaseCommand

from backend.accounts.models import User
from backend.accounts.schemas import UserSchema


class Command(BaseCommand):
    help = "Custom command to populate the data of the users in MongoDB"

    def handle(self, *args, **options):
        """
        Main entry point for the custom management command.
        """        
        User_data = UserSchema(
            username=os.environ.get('USERNAME_TEST', 'user'),
            password=os.environ.get('PASSWORD_TEST', 'pass'),
            email="admin@example.com",
            first_name="Admin",
            last_name="Admin",
            is_active=True,
        )
        User.objects.create(User_data)

        self.stdout.write(self.style.SUCCESS("User data stored in MongoDB"))
