import importlib
from django.core.management.base import BaseCommand

MIGRATIONS = [
    'backend.accounts.migrations.001_create_indexes_user',
    'backend.books.migrations.001_create_indexes_book',
]

class Command(BaseCommand):
    help = "Custom command to manage MongoDB collections and initial setup"

    def execute_migrations(self):
        """
        Executes the migrations listed in the MIGRATIONS list.
        """
        for migration in MIGRATIONS:
            try:
                module = importlib.import_module(migration)

                if not hasattr(module, 'run'):
                    self.stdout.write(self.style.ERROR(f"The {migration} module does not have a 'run' function"))
                    continue

                self.stdout.write(self.style.SUCCESS(f"Running migration: {migration}"))
                module.run()
                self.stdout.write(self.style.SUCCESS(f"Migration {migration} successfully executed"))

            except ModuleNotFoundError:
                self.stdout.write(self.style.ERROR(f"Module not found: {migration}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error while executing migration {migration}: {e}"))

    def handle(self, *args, **options):
        """
        Main entry point for the custom management command.
        """
        self.execute_migrations()
        self.stdout.write(self.style.SUCCESS("MongoDB migrations applied"))
