import json
import pytest
from typing import Final
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from coffee_roaster_market.apps.item.serializers import ItemSerializer
from coffee_roaster_market.apps.coffee.tests.assets import (
    parse_json_data,
    compare_dicts,
)
from coffee_roaster_market.apps.coffee.tests.factories import CoffeeFactory

from .factories import ItemFactory

pytestmark = pytest.mark.django_db

JSON_FORMAT: Final[str] = "json"

ITEMS_LIST: Final[str] = "item:items-list"
ITEMS_DETAIL: Final[str] = "item:items-detail"


def test_get_item(client: APIClient):
    item = ItemFactory()
    serialized = ItemSerializer(item)
    url = reverse(ITEMS_LIST)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = parse_json_data(response.content)

    assert len(response_data) == 1
    assert response_data[0] == serialized.data


def test_post_item(client: APIClient):
    coffee = CoffeeFactory()
    item = ItemFactory.build(coffee=coffee)
    serialized = ItemSerializer(item)
    url = reverse(ITEMS_LIST)
    response = client.post(url, serialized.data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_201_CREATED

    content = json.loads(response.content)

    assert content["id"] is not None
    compare_dicts(content, serialized.data, ("id",))


def test_put_item(client: APIClient):
    initial_item = ItemFactory()
    new_coffee = CoffeeFactory()
    item = ItemFactory.build(
        id=initial_item.id,
        coffee=new_coffee,
    )
    serialized = ItemSerializer(item)
    data = serialized.data
    data.pop("id")
    url = reverse(ITEMS_DETAIL, args=[item.id])
    response = client.put(url, data, format=JSON_FORMAT)

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == serialized.data


def test_delete_item(client: APIClient):
    item = ItemFactory()
    url = reverse(ITEMS_DETAIL, args=[item.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
