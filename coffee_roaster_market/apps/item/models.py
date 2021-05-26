from django.db import models

from coffee_roaster_market.apps.coffee.models import CoffeeModel


class ItemModel(models.Model):
    class Meta:
        db_table = "item"

    coffee = models.ForeignKey(CoffeeModel, on_delete=models.CASCADE)
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.coffee}, {self.price}"
