import pytest
from rest_framework.serializers import ValidationError

from ..serializers import UserCreateSerializer


def test_user_create_serializer_with_different_passwords():
    with pytest.raises(ValidationError, match="password mismatch"):
        UserCreateSerializer().validate(
            attrs={
                "username": "mee",
                "email": "hello@example.com",
                "password": "one",
                "password_retype": "two",
            }
        )
