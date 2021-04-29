import pytest

from typing import Final
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from coffee_roaster_market.apps.coffee.serializers import SensorialProfilSerializer

from .factories import SensorialProfileFactory
from .assets import parse_json_data

USERNAME: Final[str] = "someuser"
PASSWORD: Final[str] = "password"
JSON_FORMAT: Final[str] = "json"

pytestmark = pytest.mark.django_db


@pytest.fixture
def client(django_user_model: User) -> APIClient:
    django_user_model.objects.create_user(username=USERNAME, password=PASSWORD)
    user = User.objects.get(username=USERNAME)
    client = APIClient()
    client.force_authenticate(user=user)

    return client


def test_get_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    serialized = SensorialProfilSerializer(sensorial_profile)
    response = client.get("/sensorial_profiles/")

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data
