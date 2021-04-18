from django.contrib import admin
from .models import CoffeeModel, PlantationModel, SensorialProfileModel


@admin.register(CoffeeModel)
class CoffeeModelAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(PlantationModel)
admin.site.register(SensorialProfileModel)
