from django.contrib.auth.hashers import check_password
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .token import verify_token


def authenticate(username, password):
    """
    Authenticates a user by username and password.

    :param username: The username of the user.
    :param password: The user's password.
    :return: True if authenticated, None otherwise.
    """
    try:
        user = User.objects.get(username=username)
        if not user:
            return None
    except Exception:
        return None

    if check_password(password, user.password):
        user.is_authenticated = True
        user.save()
        return True

    return None


class CustomTokenAuthentication(BaseAuthentication):
    """
    Custom token-based authentication using PyMongo.
    """

    def authenticate(self, request):
        """
        Authenticates the user using a token from the Authorization header.

        :param request: The HTTP request object.
        :return: A tuple of the user and token if authentication is successful, None otherwise.
        :raises AuthenticationFailed: If the token is invalid or missing.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        is_verified, response = verify_token(token)
        if not is_verified:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.get(id=response)
        return (user, token)

    def authenticate_header(self, request):
        """
        Returns the authentication scheme used in the header.

        :param request: The HTTP request object.
        :return: The string "Bearer".
        """
        return "Bearer"
