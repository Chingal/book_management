from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserSchema(BaseModel):
    """
    Represents a user with validations in the fields.
    """

    username: str
    password: str
    email: Optional[EmailStr]
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    is_active: bool = True
    is_authenticated: bool = False
    id: Optional[str] = None

    @field_validator("username")
    def validate_username(cls, value):
        """
        Validates the username field.

        :param value: The username to validate.
        :return: The validated username.
        :raises ValueError: If the username is not alphanumeric or too short.
        """
        if not value.isalnum():
            raise ValueError("The username must only contain alphanumeric characters.")
        if len(value) < 3:
            raise ValueError("The username must have at least 3 characters.")
        return value
