import pytest
from app.models.user import AppUser

def test_user_creation():
    user = AppUser(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"