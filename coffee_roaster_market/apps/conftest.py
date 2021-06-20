import pytest

from typing import Final
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

USERNAME: Final[str] = "someuser"
PASSWORD: Final[str] = "password"


@pytest.fixture
def client(django_user_model) -> APIClient:
    user = django_user_model.objects.create_user(username=USERNAME, password=PASSWORD)
    user.is_active = True
    user.save()
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    return client


@pytest.fixture
def staff_client(django_user_model) -> APIClient:
    user = django_user_model.objects.create_user(username=USERNAME, password=PASSWORD)
    user.is_active = True
    user.is_staff = True
    user.save()
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    return client
