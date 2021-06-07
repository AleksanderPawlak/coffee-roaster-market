from django.contrib import admin

from .models import ItemModel


@admin.register(ItemModel)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ["id", "coffee", "weight", "price"]
