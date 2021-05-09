from rest_framework import serializers

from .models import (
    SensorialProfileModel,
    GeoLocationModel,
    PlantationModel,
    CoffeeModel,
)


class SensorialProfileSerializer(serializers.ModelSerializer):
    overall = serializers.ReadOnlyField()

    class Meta:
        model = SensorialProfileModel
        fields = (
            "id",
            "accidity",
            "balance",
            "body",
            "flavor",
            "aftertaste",
            "sweetness",
            "clean_cup",
            "overall",
        )


class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocationModel
        fields = "__all__"


class PlantationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantationModel
        fields = "__all__"


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeModel
        fields = "__all__"
