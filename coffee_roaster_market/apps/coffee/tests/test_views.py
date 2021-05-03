import pytest

from typing import Final
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from coffee_roaster_market.apps.coffee.serializers import (
    SensorialProfilSerializer,
    GeoLocationSerializer,
    PlantationSerializer,
    CoffeeSerializer,
)

from .factories import (
    SensorialProfileFactory,
    GeolocationFactory,
    PlantationFactory,
    CoffeeFactory,
)
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


# TODO: maybe one parametrized test for all views?


def test_get_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    serialized = SensorialProfilSerializer(sensorial_profile)
    response = client.get("/sensorial_profiles/")

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_delete_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    url = f"/sensorial_profiles/{sensorial_profile.id}/"
    response = client.delete(url)

    assert response.status_code == 204


def test_get_geolocation(client: APIClient):
    sensorial_profile = GeolocationFactory()
    serialized = GeoLocationSerializer(sensorial_profile)
    response = client.get("/geolocations/")

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_delete_geolocation(client: APIClient):
    geolocation = GeolocationFactory()
    url = f"/geolocations/{geolocation.id}/"
    response = client.delete(url)

    assert response.status_code == 204


def test_get_plantation(client: APIClient):
    sensorial_profile = PlantationFactory()
    serialized = PlantationSerializer(sensorial_profile)
    response = client.get("/plantations/")

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_delete_plantation(client: APIClient):
    plantation = PlantationFactory()
    url = f"/plantations/{plantation.id}/"
    response = client.delete(url)

    assert response.status_code == 204


def test_get_coffee(client: APIClient):
    sensorial_profile = CoffeeFactory()
    serialized = CoffeeSerializer(sensorial_profile)
    response = client.get("/coffee/")

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_delete_coffee(client: APIClient):
    coffee = CoffeeFactory()
    url = f"/coffee/{coffee.id}/"
    response = client.delete(url)

    assert response.status_code == 204
