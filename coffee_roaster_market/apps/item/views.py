from rest_framework import viewsets, permissions

from .models import ItemModel
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
