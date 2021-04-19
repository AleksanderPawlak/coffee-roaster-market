from django.contrib import admin
from .models import (
    CoffeeModel,
    GeoLocationModel,
    PlantationModel,
    SensorialProfileModel,
)


@admin.register(PlantationModel)
class PlantationModelAdmin(admin.ModelAdmin):
    list_display = ["name", "geo_location", "geolocation_plantation_height"]

    def geolocation_plantation_height(self, obj):
        return obj.geo_location.plantation_height


@admin.register(GeoLocationModel)
class GeoLocationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "country", "plantation_height"]


@admin.register(CoffeeModel)
class CoffeeModelAdmin(admin.ModelAdmin):
    list_display = ["name", "plantation", "roast_date"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SensorialProfileModel)
class SensorialProfileModelAdmin(admin.ModelAdmin):
    readonly_fields = ["overall"]
