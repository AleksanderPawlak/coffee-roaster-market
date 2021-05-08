import pytest

from coffee_roaster_market.apps.coffee.models import (
    SensorialProfileModel,
    GeoLocationModel,
    PlantationModel,
    CoffeeModel,
)
from coffee_roaster_market.apps.coffee.serializers import (
    SensorialProfileSerializer,
    GeoLocationSerializer,
    PlantationSerializer,
    CoffeeSerializer,
)

from .factories import GeolocationFactory, PlantationFactory, SensorialProfileFactory
from .assets import parse_json_data

pytestmark = pytest.mark.django_db


def test_sensorial_profile_serializer():
    expected_overall = 10
    data = b"""{
        "accidity": 10,
        "balance": 10,
        "body": 10,
        "flavor": 10,
        "aftertaste": 10,
        "sweetness": 10,
        "clean_cup": 10
    }"""
    data_dict = parse_json_data(data)
    serializer = SensorialProfileSerializer(data=data_dict)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert SensorialProfileModel.objects.all().last() == object_

    serialized_object = SensorialProfileSerializer(object_)
    data_dict["overall"] = expected_overall
    data_dict["id"] = object_.id

    assert serialized_object.data == data_dict


def test_geolocation_serializer():
    data = b"""{
        "plantation_height": 10.0,
        "longitude": 10.11,
        "latitude": 11.2,
        "country": "Poland"
    }"""
    data_dict = parse_json_data(data)
    serializer = GeoLocationSerializer(data=data_dict)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert GeoLocationModel.objects.all().last() == object_

    serialized_object = GeoLocationSerializer(object_)
    data_dict["id"] = object_.id

    assert serialized_object.data == data_dict


def test_plantation_serializer():
    geo_location = GeolocationFactory.create()
    data = f"""{{
        "name": "Giorgione",
        "geo_location": {geo_location.id}
    }}""".encode()

    data_dict = parse_json_data(data)
    serializer = PlantationSerializer(data=data_dict)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert PlantationModel.objects.all().last() == object_

    serialized_object = PlantationSerializer(object_)
    data_dict["id"] = object_.id

    assert serialized_object.data == data_dict


def test_coffee_serializer():
    sensorial_profile = SensorialProfileFactory.create()
    plantation = PlantationFactory.create()
    data = f"""{{
        "name": "Kopi luwak",
        "slug": "some slug",
        "description": "Partially digested coffee cherries",
        "processing_method": "natural",
        "roast_date": "2021-02-01",
        "sensorial_profile": {sensorial_profile.id},
        "plantation": {plantation.id}
    }}""".encode()

    data_dict = parse_json_data(data)
    serializer = CoffeeSerializer(data=data_dict)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert CoffeeModel.objects.all().last() == object_

    serialized_object = CoffeeSerializer(object_)
    data_dict["id"] = object_.id

    assert serialized_object.data == data_dict
