import pytest

from coffee_roaster_market.apps.item.serializers import ItemSerializer
from coffee_roaster_market.apps.item.models import ItemModel

from coffee_roaster_market.apps.coffee.tests.assets import parse_json_data
from coffee_roaster_market.apps.coffee.tests.factories import CoffeeFactory

pytestmark = pytest.mark.django_db


def test_item_serializer():
    coffee = CoffeeFactory.create()
    data = f"""{{
        "coffee": {coffee.id},
        "weight": 111.123,
        "price": 11.88
    }}
    """.encode()

    data = parse_json_data(data)
    serializer = ItemSerializer(data=data)

    assert serializer.is_valid()

    object_ = serializer.save()

    assert ItemModel.objects.all().last() == object_

    serialized_object = ItemSerializer(object_)
    object_data = serialized_object.data

    assert object_data["coffee"] == coffee.id
    assert object_data["weight"] == 111.123
    assert object_data["price"] == "11.88"
