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
    SensorialProfileSerializer,
)


class SensorialProfileViewSet(viewsets.ModelViewSet):
    queryset = SensorialProfileModel.objects.all()
    serializer_class = SensorialProfileSerializer
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
