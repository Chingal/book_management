from bson import ObjectId
from datetime import datetime, date

from backend.mongodb import db


class BookManager:
    """
    Manages book operations such as creation and uniqueness checks.
    """

    def __init__(self):
        """
        Initializes the BookManager with the 'books' collection.
        """
        self.collection = db["books"]

    @property
    def raw_collection(self):
        """
        Provides direct access to the MongoDB collection.
        :return: The MongoDB collection object.
        """
        return self.collection

    def update(self, book_id, data):
        """
        Update a book document in MongoDB by its ID.
        :param book_id: The ID of the book to update.
        :param data: A dictionary with the updated fields.
        :return: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise ValueError(f"Error updating book: {str(e)}")

    def create(self, book):
        """
        Create a book in the database.

        :param book: The book object to be created.
        :raises ValueError: If the username already exists and a new book is being created.
        """
        book_data = {
            "title": book.title,
            "author": book.author,
            "published_date": (
                datetime.combine(book.published_date, datetime.min.time())
                if isinstance(book.published_date, date)
                else book.published_date
            ),
            "genre": book.genre,
            "price": book.price
        }

        if not book.id:
            document = self.collection.insert_one(book_data)
            book.id = str(document.inserted_id)
        else:
            self.collection.replace_one(
                {"_id": ObjectId(book.id)},
                book_data,
                upsert=True
            )

    def get(self, **kwargs):
        """
        Retrieves a single book document based on the provided filters.
        """
        from backend.books.models import Book
        if "id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs.pop("id"))
        document = self.collection.find_one(kwargs)
        return Book(**document) if document else None

    def all(self, filter_query=None):
        """
        Retrieves all book documents that match the given filter query.
        """
        from backend.books.models import Book
        filter_query = {
            key: {'$regex': value, '$options': 'i'}
            for key, value in (filter_query or {}).items()
        }
        documents = self.collection.find(filter_query)
        return [
            Book(
                _id=str(doc["_id"]),
                title=doc.get("title", "Untitled"),
                author=doc.get("author", "Author unknown"),
                published_date=(
                    doc["published_date"].date()
                    if isinstance(doc["published_date"], datetime)
                    else doc.get("published_date")
                ),
                genre=doc.get("genre", "Unknown"),
                price=doc.get("price", 0.0)
            )
            for doc in documents
        ]

    def delete(self, book_id):
        """
        Delete a book by its ID in MongoDB.
        """
        result = self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0
