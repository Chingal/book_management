import pytest
from pydantic import ValidationError

from backend.accounts.schemas import UserSchema

def test_valid_user_creation():
    """Test that a valid user is created successfully"""
    user = UserSchema(
        username="validuser",
        password="passwordtest",
        email="validuser@example.com",
        first_name="Pepito",
        last_name="Perez"
    )
    assert user.username == "validuser"
    assert user.password == "passwordtest"
    assert user.email == "validuser@example.com"
    assert user.first_name == "Pepito"
    assert user.last_name == "Perez"
    assert user.is_active is True
    assert user.id is None

def test_invalid_username_non_alphanumeric():
    """Test that a username with non-alphanumeric characters raises a ValueError"""
    with pytest.raises(ValidationError) as exc_info:
        UserSchema(
            username="invalid$user",
            email="user@example.com"
        )

    assert "The username must only contain alphanumeric characters." in str(exc_info.value)

def test_invalid_username_too_short():
    """Test that a username with fewer than 3 characters raises a ValueError"""
    with pytest.raises(ValidationError) as exc_info:
        UserSchema(
            username="ab",
            password="passwordtest",
            email="user@example.com"
        )

    assert "The username must have at least 3 characters." in str(exc_info.value)

def test_invalid_email():
    """Test that an invalid email raises a ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        UserSchema(
            username="validuser",
            password="passwordtest",
            email="invalid-email"
        )

    assert "value is not a valid email address" in str(exc_info.value)

def test_default_values():
    """Test that default values are correctly assigned"""
    user = UserSchema(
        username="defaultuser",
        password="passwordtest",
        email="default@example.com"
    )
    assert user.first_name == ""
    assert user.last_name == ""
    assert user.is_active is True
    assert user.id is None

def test_optional_id_field():
    """Test that the optional 'id' field can be set"""
    user = UserSchema(
        username="validuser",
        password="passwordtest",
        email="user@example.com",
        id="123456789",
    )
    assert user.id == "123456789"
