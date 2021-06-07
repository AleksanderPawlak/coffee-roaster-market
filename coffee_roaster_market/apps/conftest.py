import pytest

from typing import Final
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


USERNAME: Final[str] = "someuser"
PASSWORD: Final[str] = "password"


@pytest.fixture
def client(django_user_model: User) -> APIClient:
    user = django_user_model.objects.create_user(username=USERNAME, password=PASSWORD)
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    return client
