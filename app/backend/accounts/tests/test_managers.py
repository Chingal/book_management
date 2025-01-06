import pytest
from bson import ObjectId
from django.contrib.auth.hashers import make_password

from backend.accounts.managers import UserManager

@pytest.fixture
def db(mocker):
    """Fixture to mock the database collection."""
    return mocker.patch("backend.accounts.managers.db")

@pytest.fixture
def user_manager(db):
    """Fixture to provide a UserManager with a mocked database."""
    return UserManager()

@pytest.fixture
def mock_user(mocker):
    """Fixture to provide a mock user."""
    user = mocker.MagicMock()
    user.username = "testuser"
    user.password = "superpass"
    user.email = "test@example.com"
    user.first_name = "Test"
    user.last_name = "User"
    user.is_active = True
    user.id = None
    return user

def test_is_username_unique_true(user_manager, db):
    """Test that is_username_unique returns True if username is unique."""
    db["users"].find_one.return_value = None

    result = user_manager.is_username_unique("unique_username")
    assert result is True
    db["users"].find_one.assert_called_once_with({"username": "unique_username"})

def test_is_username_unique_false(user_manager, db):
    """Test that is_username_unique returns False if username exists."""
    db["users"].find_one.return_value = {"username": "existing_username"}

    result = user_manager.is_username_unique("existing_username")
    assert result is False
    db["users"].find_one.assert_called_once_with({"username": "existing_username"})


def test_create_existing_user_raises_error(user_manager, db, mock_user):
    """Test that create raises ValueError if username already exists."""
    db["users"].find_one.return_value = {"username": "testuser"}

    with pytest.raises(ValueError, match="El username 'testuser' ya existe."):
        user_manager.create(mock_user)

    db["users"].find_one.assert_called_once_with({"username": "testuser"})
    db["users"].insert_one.assert_not_called()
