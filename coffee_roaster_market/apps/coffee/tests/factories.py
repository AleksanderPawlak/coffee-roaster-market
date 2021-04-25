import factory
import factory.fuzzy
from django.template.defaultfilters import slugify
from django.utils import timezone

from coffee_roaster_market.apps.coffee.models import (
    CoffeeModel,
    GeoLocationModel,
    PlantationModel,
    SensorialProfileModel,
)


class SensorialProfileFactory(factory.django.DjangoModelFactory):
    accidity = factory.fuzzy.FuzzyInteger(low=0, high=100)
    balance = factory.fuzzy.FuzzyInteger(low=0, high=100)
    body = factory.fuzzy.FuzzyInteger(low=0, high=100)
    flavor = factory.fuzzy.FuzzyInteger(low=0, high=100)
    aftertaste = factory.fuzzy.FuzzyInteger(low=0, high=100)
    sweetness = factory.fuzzy.FuzzyInteger(low=0, high=100)
    clean_cup = factory.fuzzy.FuzzyInteger(low=0, high=100)

    class Meta:
        model = SensorialProfileModel


class GeolocationFactory(factory.django.DjangoModelFactory):
    plantation_height = factory.fuzzy.FuzzyFloat(low=0, precision=2)
    longitude = factory.fuzzy.FuzzyFloat(low=0, precision=2)
    latitude = factory.fuzzy.FuzzyFloat(low=0, precision=2)
    country = factory.Faker("country_code")

    class Meta:
        model = GeoLocationModel


class PlantationFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    geo_location = factory.SubFactory(GeolocationFactory)

    class Meta:
        model = PlantationModel


class CoffeeFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    processing_method = factory.fuzzy.FuzzyChoice(
        [x[0] for x in CoffeeModel.ProcessingMethod.choices]
    )
    sensorial_profile = factory.SubFactory(SensorialProfileFactory)
    plantation = factory.SubFactory(PlantationFactory)
    roast_date = factory.fuzzy.FuzzyDate(
        start_date=timezone.datetime(1990, 2, 7), end_date=timezone.datetime.today()
    )

    class Meta:
        model = CoffeeModel
