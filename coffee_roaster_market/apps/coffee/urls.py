from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(
    r"sensorial_profiles", views.SensorialProfileViewSet, basename="sensorial_profiles"
)
router.register(r"geolocations", views.GeolocationViewSet, basename="geolocations")
router.register(r"plantations", views.PlantationViewSet, basename="plantations")
router.register(r"coffee", views.CoffeeViewSet, basename="coffee")

app_name = "coffee"

urlpatterns = [
    path("", include(router.urls)),
]
