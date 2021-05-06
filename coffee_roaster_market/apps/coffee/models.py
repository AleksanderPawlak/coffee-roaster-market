from django.core.validators import MaxValueValidator
from django.db import models
from django.forms.models import model_to_dict


class SensorialProfileModel(models.Model):
    accidity = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    balance = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    body = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    flavor = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    aftertaste = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    sweetness = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    clean_cup = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

    # overall will be calculated from other fields
    @property
    def overall(self) -> int:
        model_dict = model_to_dict(self, exclude=["id"])
        return round(sum(v for v in model_dict.values()) / len(model_dict))

    def __str__(self) -> str:
        return f"{self.pk}. Overall value: {self.overall}"


class GeoLocationModel(models.Model):
    plantation_height = models.FloatField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    country = models.CharField(max_length=60)  # Country field

    #  Todo:  Other Fields, address as different table...
    def __str__(self) -> str:
        return f"{self.country}, height: {self.plantation_height}"


class PlantationModel(models.Model):
    name = models.CharField(max_length=80)
    geo_location = models.ForeignKey(GeoLocationModel, on_delete=models.CASCADE)

    # Address - different table
    def __str__(self) -> str:
        return f"{self.name}"


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
    description = models.TextField(blank=True)
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

    def __str__(self) -> str:
        return f"{self.name}, {self.plantation}"

    # Roaster foreign key will be also possible
