import pytest
from backend.accounts.auth import authenticate

def test_authenticate_user_not_found(mocker):
    username = "nonexistent_user"
    password = "password123"
    mocker.patch("backend.accounts.models.User.objects.get", side_effect=Exception)
    result = authenticate(username, password)
    assert result is None, "Should return None for a non-existent user"

def test_authenticate_incorrect_password(mocker):
    username = "testuser"
    password = "correct_password"
    wrong_password = "wrong_password"

    mock_user = mocker.Mock()
    mock_user.password = "hashed_password"
    mocker.patch("backend.accounts.models.User.objects.get", return_value=mock_user)
    mocker.patch("django.contrib.auth.hashers.check_password", return_value=False)

    result = authenticate(username, wrong_password)
    assert result is None, "Should return None for incorrect password"
