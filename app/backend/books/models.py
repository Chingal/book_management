from django.conf import settings

from .managers import BookManager
from .schemas import BookSchema

class Book:
    """
    Represents a book with basic attributes like title, author, published_date, genre, price
    """
    objects = BookManager()

    def __init__(self, title, author, price, published_date=None, genre=None, _id=None):
        """
        Initializes a Book instance.

        :param title: The title of the book
        :param author: The author of the book
        :param published_date: The publication date of the book
        :param genre: The genre of the book
        :param price: The price of the book (must be positive)
        :param _id: The unique identifier for the book (optional).
        """
        self.id = str(_id) if _id else None
        self.title = title
        self.author = author
        self.published_date = published_date
        self.genre = genre
        self.price = price

    def save(self):
        """
        Saves the current book instance using the BookManager.
        """
        book_data = BookSchema(
            title=self.title,
            author=self.author,
            published_date=self.published_date,
            genre=self.genre,
            price=self.price,
            id=self.id
        )
        Book.objects.create(book_data)
