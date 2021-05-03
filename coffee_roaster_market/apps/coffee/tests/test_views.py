import pytest
import json

from typing import Final, Optional, Iterable
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

SENSORIAL_PROFILES_URL: Final[str] = "/sensorial_profiles/"
GEOLOCATIONS_URL: Final[str] = "/geolocations/"
PLANTATIONS_URL: Final[str] = "/plantations/"
COFFEE_URL: Final[str] = "/coffee/"

pytestmark = pytest.mark.django_db


def compare_dicts(
    value: dict, expected_value: dict, exclude_fields: Optional[Iterable[str]] = None
) -> None:
    exclude_fields = exclude_fields or []
    keys = (key for key in expected_value if key not in exclude_fields)
    for key in keys:
        assert value[key] == expected_value[key]


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
    response = client.get(SENSORIAL_PROFILES_URL)

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory.build()
    serialized = SensorialProfilSerializer(sensorial_profile)
    response = client.post(SENSORIAL_PROFILES_URL, serialized.data, format=JSON_FORMAT)

    assert response.status_code == 201

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_sensorial_profile(client: APIClient):
    initial_sensorial_profile = SensorialProfileFactory()
    sensorial_profile = SensorialProfileFactory.build(id=initial_sensorial_profile.id)
    serialized = SensorialProfilSerializer(sensorial_profile)
    data = serialized.data
    data.pop("id")
    url = f"{SENSORIAL_PROFILES_URL}{sensorial_profile.id}/"
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == 200
    assert json.loads(response.content) == serialized.data


def test_delete_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    url = f"{SENSORIAL_PROFILES_URL}{sensorial_profile.id}/"
    response = client.delete(url)

    assert response.status_code == 204


def test_get_geolocation(client: APIClient):
    geo_location = GeolocationFactory()
    serialized = GeoLocationSerializer(geo_location)
    response = client.get(GEOLOCATIONS_URL)

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_geolocation(client: APIClient):
    geo_location = GeolocationFactory.build()
    serialized = GeoLocationSerializer(geo_location)
    response = client.post(GEOLOCATIONS_URL, serialized.data, format=JSON_FORMAT)

    assert response.status_code == 201

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_geolocation(client: APIClient):
    initial_geo_location = GeolocationFactory()
    geo_location = GeolocationFactory.build(id=initial_geo_location.id)
    serialized = GeoLocationSerializer(geo_location)
    data = serialized.data
    data.pop("id")
    url = f"{GEOLOCATIONS_URL}{geo_location.id}/"
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == 200
    assert json.loads(response.content) == serialized.data


def test_delete_geolocation(client: APIClient):
    geo_location = GeolocationFactory()
    url = f"{GEOLOCATIONS_URL}{geo_location.id}/"
    response = client.delete(url)

    assert response.status_code == 204


def test_get_plantation(client: APIClient):
    plantation = PlantationFactory()
    serialized = PlantationSerializer(plantation)
    response = client.get(PLANTATIONS_URL)

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_plantation(client: APIClient):
    geo_location = GeolocationFactory()
    plantation = PlantationFactory.build(geo_location=geo_location)
    serialized = PlantationSerializer(plantation)
    response = client.post(PLANTATIONS_URL, serialized.data, format=JSON_FORMAT)

    assert response.status_code == 201

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_plantation(client: APIClient):
    initial_plantation = PlantationFactory()
    new_geo_location = GeolocationFactory()
    plantation = PlantationFactory.build(
        id=initial_plantation.id, geo_location=new_geo_location
    )
    serialized = PlantationSerializer(plantation)
    data = serialized.data
    data.pop("id")
    url = f"{PLANTATIONS_URL}{plantation.id}/"
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == 200
    assert json.loads(response.content) == serialized.data


def test_delete_plantation(client: APIClient):
    plantation = PlantationFactory()
    url = f"{PLANTATIONS_URL}{plantation.id}/"
    response = client.delete(url)

    assert response.status_code == 204


def test_get_coffee(client: APIClient):
    coffee = CoffeeFactory()
    serialized = CoffeeSerializer(coffee)
    response = client.get(COFFEE_URL)

    assert response.status_code == 200

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_coffee(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    plantation = PlantationFactory()
    coffee = CoffeeFactory.build(
        sensorial_profile=sensorial_profile, plantation=plantation
    )
    serialized = CoffeeSerializer(coffee)
    response = client.post(COFFEE_URL, serialized.data, format=JSON_FORMAT)

    assert response.status_code == 201

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_coffee(client: APIClient):
    initial_coffee = CoffeeFactory()
    new_sensorial_profile = SensorialProfileFactory()
    new_plantation = PlantationFactory()
    coffee = CoffeeFactory.build(
        id=initial_coffee.id,
        sensorial_profile=new_sensorial_profile,
        plantation=new_plantation,
    )
    serialized = CoffeeSerializer(coffee)
    data = serialized.data
    data.pop("id")
    url = f"{COFFEE_URL}{coffee.id}/"
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == 200
    assert json.loads(response.content) == serialized.data


def test_delete_coffee(client: APIClient):
    coffee = CoffeeFactory()
    url = f"{COFFEE_URL}{coffee.id}/"
    response = client.delete(url)

    assert response.status_code == 204
