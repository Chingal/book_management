from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.accounts.models import User
from backend.accounts.auth import authenticate
from backend.accounts.token import generate_token

from .serializers import LoginSerializer

class CustomLoginView(APIView):
    """Class to authenticate a user via auth/login"""
    permission_classes = (AllowAny,)
    name = 'Auth Login'

    @staticmethod
    def validate_fields(username, password):
        """
        Validate that the required fields are not empty.

        :param username: str
        :param password: str
        :return: dict or None
        """
        if not username:
            return {'error': 'Username field is required'}
        if not password:
            return {'error': 'Password field is required'}
        return None

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Authentication successful",
                examples={
                    "application/json": {
                        "token_type": "Bearer",
                        "access_token": "your_access_token"
                    }
                },
            ),
            400: openapi.Response(description="Validation error"),
            401: openapi.Response(description="Invalid credentials"),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Handle user login requests.

        :param request: HTTP request object
        :return: Response object with authentication token or error message
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # Authenticate user
        if authenticate(username=username, password=password):
            user = User.objects.get(username=username)
            auth_token = {
                'token_type': 'Bearer',
                'access_token': generate_token(user.id)
            }
            return Response(auth_token, status=status.HTTP_200_OK)

        # Return error if authentication fails
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )