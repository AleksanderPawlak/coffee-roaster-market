from rest_framework import viewsets, permissions

from .models import (
    CoffeeModel,
    PlantationModel,
    GeoLocationModel,
    SensorialProfileModel,
)
from .serializers import (
    CoffeeSerializer,
    PlantationSerializer,
    GeoLocationSerializer,
    SensorialProfilSerializer,
)


class SensorialProfileViewSet(viewsets.ModelViewSet):
    queryset = SensorialProfileModel.objects.all()
    serializer_class = SensorialProfilSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GeolocationViewSet(viewsets.ModelViewSet):
    queryset = GeoLocationModel.objects.all()
    serializer_class = GeoLocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PlantationViewSet(viewsets.ModelViewSet):
    queryset = PlantationModel.objects.all()
    serializer_class = PlantationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CoffeeViewSet(viewsets.ModelViewSet):
    queryset = CoffeeModel.objects.all()
    serializer_class = CoffeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
