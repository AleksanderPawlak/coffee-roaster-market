import factory
import factory.fuzzy

from coffee_roaster_market.apps.item.models import ItemModel
from coffee_roaster_market.apps.coffee.tests.factories import CoffeeFactory


class ItemFactory(factory.django.DjangoModelFactory):
    coffee = factory.SubFactory(CoffeeFactory)
    weight = factory.fuzzy.FuzzyFloat(low=0)
    price = factory.fuzzy.FuzzyDecimal(low=0)

    class Meta:
        model = ItemModel
