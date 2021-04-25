import io
import pytest

from rest_framework.parsers import JSONParser

from coffee_roaster_market.apps.coffee.models import (
    SensorialProfileModel,
    GeoLocationModel,
    PlantationModel,
    CoffeeModel,
)
from coffee_roaster_market.apps.coffee.serializers import (
    SensorialProfilSerializer,
    GeoLocationSerializer,
    PlantationSerializer,
    CoffeeSerializer,
)

pytestmark = pytest.mark.django_db


def prepare_data(json_data: bytes) -> dict:
    stream = io.BytesIO(json_data)
    return JSONParser().parse(stream)


def test_sensorial_profile_serialize():
    data = b"""{
        "accidity": 10,
        "balance": 10,
        "body": 10,
        "flavor": 10,
        "aftertaste": 10,
        "sweetness": 10,
        "clean_cup": 10
    }"""
    prepared_data = prepare_data(data)
    serializer = SensorialProfilSerializer(data=prepared_data)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert SensorialProfileModel.objects.all().last() == object_


def test_geolocation_serializer():
    data = b"""{
        "plantation_height": 10.0,
        "longitude": 10.11,
        "latitude": 11.2,
        "country": "Poland"
    }"""
    prepared_data = prepare_data(data)
    serializer = GeoLocationSerializer(data=prepared_data)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert GeoLocationModel.objects.all().last() == object_


def test_plantation_serializer():
    data = b"""{
        "name": "Giorgione",
        "geo_location": 1
    }"""
    prepared_data = prepare_data(data)
    serializer = PlantationSerializer(data=prepared_data)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert PlantationModel.objects.all().last() == object_


def test_coffee_serializer():
    data = b"""{
        "name": "Kopi luwak",
        "slug": "something",
        "description": "Partially digested coffee cherries",
        "processing_method": "natural",
        "roast_date": "2021-02-01",
        "sensorial_profile": 1,
        "plantation": 1
    }"""
    prepared_data = prepare_data(data)
    serializer = CoffeeSerializer(data=prepared_data)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert CoffeeModel.objects.all().last() == object_
