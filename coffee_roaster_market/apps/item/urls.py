from django.urls import path, include
from rest_framework import routers

from . import views

app_name = "item"

router = routers.DefaultRouter()
router.register(r"items", views.ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
]
