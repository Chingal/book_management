import random

from django.core.management.base import BaseCommand
from faker import Faker

from backend.books.models import Book
from backend.books.schemas import BookSchema


class Command(BaseCommand):
    help = "Custom command to populate the data of the books in MongoDB"

    def handle(self, *args, **options):
        """
        Main entry point for the custom management command.
        """
        faker = Faker()

        for _ in range(10):
            book_data = BookSchema(
                title=faker.sentence(nb_words=10),
                author=faker.name(),
                published_date=faker.date_this_century(),
                genre=random.choice(["Fiction", "Non-fiction", "Fantasy", "Biography", "Mystery", "Science Fiction", "Romance"]),
                price=round(random.uniform(5.0, 50.0), 2)
            )
            Book.objects.create(book_data)

        self.stdout.write(self.style.SUCCESS("Book data stored in MongoDB"))
