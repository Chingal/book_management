from bson import ObjectId
from django.conf import settings

from .managers import UserManager
from .schemas import UserSchema


class User:
    """
    Represents a user with basic attributes like username, email, and first and last name.
    """
    objects = UserManager()

    def __init__(self, username, password, email, first_name="", last_name="", is_active=True, _id=None, is_authenticated=False):
        """
        Initializes a User instance.

        :param username: The username of the user.
        :param password: The password of the user.
        :param email: The email of the user.
        :param first_name: The first name of the user (optional).
        :param last_name: The last name of the user (optional).
        :param is_active: Whether the user is active (default: True).
        :param _id: The unique identifier for the user (optional).
        """
        self.id = str(_id) if _id else None
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_authenticated = is_authenticated

    def save(self):
        """
        Saves the current user instance using the UserManager.
        """
        user_data = UserSchema(
            username=self.username,
            password=self.password,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=self.is_active,
            is_authenticated=self.is_authenticated,
            id=self.id
        )
        User.objects.create(user_data)
