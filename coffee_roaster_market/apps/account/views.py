from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import UserSerializer, UserCreateSerializer

user = get_user_model()


class ApiUsersView(viewsets.ModelViewSet):
    queryset = user.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
