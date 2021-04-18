from django.db import models


class SensorialProfileModel(models.Model):
    accidity = models.FloatField()
    balance = models.FloatField()
    body = models.FloatField()
    flavor = models.FloatField()
    aftertaste = models.FloatField()
    sweetness = models.FloatField()
    clean_cup = models.FloatField()
    # overall will be calculated from other fields


class GeoLocationModel(models.Model):
    plantation_height = models.FloatField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    country = models.CharField(max_length=60)  # Country field

    # Other Fields, address as different table...


class PlantationModel(models.Model):
    name = models.CharField(max_length=80)
    geo_location = models.ForeignKey(GeoLocationModel, on_delete=models.CASCADE)

    # Address - different table


class CoffeeModel(models.Model):
    # Already roasted - for now it will be ok

    class ProcessingMethod(models.TextChoices):
        WASHED = "washed", "Washed"
        DRY = "dry", "Dry"
        NATURAL = "natural", "Natural"
        HONEY = "honey", "Honey"
        UNSPECIFIED = "unspecified", "Unspecified"

    name = models.CharField(max_length=80)
    slug = models.CharField(max_length=80)
    descrption = models.TextField(blank=True)
    processing_method = models.CharField(
        "ProcessingMethod",
        max_length=20,
        choices=ProcessingMethod.choices,
        default=ProcessingMethod.UNSPECIFIED,
    )
    sensorial_profile = models.ForeignKey(
        SensorialProfileModel, on_delete=models.SET_NULL, null=True
    )
    plantation = models.ForeignKey(PlantationModel, on_delete=models.CASCADE)
    roast_date = models.DateField()

    # Roaster foreign key will be also possible
