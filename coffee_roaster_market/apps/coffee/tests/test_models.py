import pytest

from .factories import CoffeeFactory, PlantationFactory

pytestmark = pytest.mark.django_db


def test_coffee_model_string_representation():
    coffee = CoffeeFactory.build(
        name="Inka", plantation=PlantationFactory.build(name="biedronesko")
    )
    assert str(coffee) == "Inka, biedronesko"
