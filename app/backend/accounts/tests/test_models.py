import pytest
from bson import ObjectId
from django.contrib.auth.hashers import check_password

from backend.accounts.models import User

@pytest.fixture
def mock_manager(mocker):
    """Fixture to mock the UserManager"""
    return mocker.patch("backend.accounts.models.User.objects")

def test_user_creation(mock_manager):
    """Test that a User instance is initialized correctly."""
    user = User(
        username="testuser",
        password="passwordtest",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
        _id=ObjectId()
    )

    assert user.username == "testuser"
    assert user.password == "passwordtest"
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.is_active is True
    assert isinstance(user.id, str)

def test_user_save(mock_manager):
    """Test that the User.save() method calls the UserManager correctly"""
    mock_create = mock_manager.create

    user = User(
        username="testuser",
        password="passwordtest",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True
    )

    user.save()

    mock_create.assert_called_once()
    args, kwargs = mock_create.call_args

    user_data = args[0]
    assert user_data.username == "testuser"
    assert user_data.password == "passwordtest"
    assert user_data.email == "test@example.com"
    assert user_data.first_name == "Test"
    assert user_data.last_name == "User"
    assert user_data.is_active is True
    assert user_data.id is None

def test_user_save_with_id(mock_manager):
    """Test that the User.save() method works correctly when the user has an ID"""
    mock_create = mock_manager.create

    user_id = str(ObjectId())
    user = User(
        username="testuser",
        password="passwordtest",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
        _id=user_id
    )

    user.save()

    mock_create.assert_called_once()
    args, _ = mock_create.call_args

    user_data = args[0]
    assert user_data.id == user_id