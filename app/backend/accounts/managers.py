from bson import ObjectId
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from backend.mongodb import db


class UserManager:
    """
    Manages user operations such as creation and uniqueness checks.
    """

    def __init__(self):
        """
        Initializes the UserManager with the 'users' collection.
        """
        self.collection = db["users"]

    def is_username_unique(self, username):
        """
        Checks if a username is unique in the database.

        :param username: The username to check.
        :return: True if the username is unique, False otherwise.
        """
        return not self.collection.find_one({"username": username})

    def _prepare_password(self, password, user_id=None):
        """Method to hash password"""
        if user_id is None or not password.startswith("pbkdf2_"):
            return make_password(password)

        return password

    def create(self, user):
        """
        Create a user in the database.

        :param user: The user object to be created.
        :raises ValueError: If the username already exists and a new user is being created.
        """
        user_data = {
            "username": user.username,
            "password": self._prepare_password(user.password, user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_authenticated": user.is_authenticated,
        }

        if not user.id:
            validate_password(user.password, user=None)

            if not self.is_username_unique(user.username):
                raise ValueError(f"El username '{user.username}' ya existe.")

            document = self.collection.insert_one(user_data)
            user.id = str(document.inserted_id)
        else:
            self.collection.replace_one(
                {"_id": ObjectId(user.id)},
                user_data,
                upsert=True
            )

    def get(self, **kwargs):
        from backend.accounts.models import User
        if "id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs.pop("id"))
        document = self.collection.find_one(kwargs)
        return User(**document) if document else None
