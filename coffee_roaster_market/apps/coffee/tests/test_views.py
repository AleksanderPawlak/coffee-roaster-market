import pytest
import json

from typing import Final
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient

from coffee_roaster_market.apps.coffee.serializers import (
    SensorialProfileSerializer,
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
from .assets import parse_json_data, compare_dicts

JSON_FORMAT: Final[str] = "json"

SENSORIAL_PROFILES_LIST: Final[str] = "coffee:sensorial_profiles-list"
SENSORIAL_PROFILES_detail: Final[str] = "coffee:sensorial_profiles-detail"
GEOLOCATIONS_LIST: Final[str] = "coffee:geolocations-list"
GEOLOCATIONS_DETAIL: Final[str] = "coffee:geolocations-detail"
PLANTATIONS_LIST: Final[str] = "coffee:plantations-list"
PLANTATIONS_DETAIL: Final[str] = "coffee:plantations-detail"
COFFEE_LIST: Final[str] = "coffee:coffee-list"
COFFEE_DETAIL: Final[str] = "coffee:coffee-detail"

pytestmark = pytest.mark.django_db


def test_get_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    serialized = SensorialProfileSerializer(sensorial_profile)
    url = reverse(SENSORIAL_PROFILES_LIST)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory.build()
    serialized = SensorialProfileSerializer(sensorial_profile)
    url = reverse(SENSORIAL_PROFILES_LIST)
    response = client.post(url, serialized.data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_201_CREATED

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_sensorial_profile(client: APIClient):
    initial_sensorial_profile = SensorialProfileFactory()
    sensorial_profile = SensorialProfileFactory.build(id=initial_sensorial_profile.id)
    serialized = SensorialProfileSerializer(sensorial_profile)
    data = serialized.data
    data.pop("id")
    url = reverse(SENSORIAL_PROFILES_detail, args=[sensorial_profile.id])
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == serialized.data


def test_delete_sensorial_profile(client: APIClient):
    sensorial_profile = SensorialProfileFactory()
    url = reverse(SENSORIAL_PROFILES_detail, args=[sensorial_profile.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_geolocation(client: APIClient):
    geo_location = GeolocationFactory()
    serialized = GeoLocationSerializer(geo_location)
    url = reverse(GEOLOCATIONS_LIST)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_geolocation(client: APIClient):
    geo_location = GeolocationFactory.build()
    serialized = GeoLocationSerializer(geo_location)
    url = reverse(GEOLOCATIONS_LIST)
    response = client.post(url, serialized.data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_201_CREATED

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_geolocation(client: APIClient):
    initial_geo_location = GeolocationFactory()
    geo_location = GeolocationFactory.build(id=initial_geo_location.id)
    serialized = GeoLocationSerializer(geo_location)
    data = serialized.data
    data.pop("id")
    url = reverse(GEOLOCATIONS_DETAIL, args=[geo_location.id])
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == serialized.data


def test_delete_geolocation(client: APIClient):
    geo_location = GeolocationFactory()
    url = reverse(GEOLOCATIONS_DETAIL, args=[geo_location.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_plantation(client: APIClient):
    plantation = PlantationFactory()
    serialized = PlantationSerializer(plantation)
    url = reverse(PLANTATIONS_LIST)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_plantation(client: APIClient):
    geo_location = GeolocationFactory()
    plantation = PlantationFactory.build(geo_location=geo_location)
    serialized = PlantationSerializer(plantation)
    url = reverse(PLANTATIONS_LIST)
    response = client.post(url, serialized.data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_201_CREATED

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
    url = reverse(PLANTATIONS_DETAIL, args=[plantation.id])
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == serialized.data


def test_delete_plantation(client: APIClient):
    plantation = PlantationFactory()
    url = reverse(PLANTATIONS_DETAIL, args=[plantation.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_coffee(client: APIClient):
    coffee = CoffeeFactory()
    serialized = CoffeeSerializer(coffee)
    url = reverse(COFFEE_LIST)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

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
    url = reverse(COFFEE_LIST)
    response = client.post(url, serialized.data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_201_CREATED

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
    url = reverse(COFFEE_DETAIL, args=[coffee.id])
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == serialized.data


def test_delete_coffee(client: APIClient):
    coffee = CoffeeFactory()
    url = reverse(COFFEE_DETAIL, args=[coffee.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
