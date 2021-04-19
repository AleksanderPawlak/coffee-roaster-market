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

    def overall(self) -> float:
        return round(
            (
                self.accidity
                + self.balance
                + self.body
                + self.flavor
                + self.aftertaste
                + self.sweetness
                + self.clean_cup
            )
            / 7,
            ndigits=2,
        )

    def __str__(self) -> str:
        return f"{self.pk}. Overall value: ..."


class GeoLocationModel(models.Model):
    plantation_height = models.FloatField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    country = models.CharField(max_length=60)  # Country field

    # Other Fields, address as different table...
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

    def __str__(self) -> str:
        return f"{self.name} r!{self.plantation}"

    # Roaster foreign key will be also possible
