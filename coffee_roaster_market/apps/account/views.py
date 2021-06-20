from typing import Iterable, Union, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import serializers

from .serializers import UserActivationSerializer, UserSerializer, UserCreateSerializer
from .permissions import CurrentUserOrAdmin

user = get_user_model()


class ApiUsersView(viewsets.ModelViewSet):
    queryset = user.objects.all()

    def get_serializer_class(self) -> Type[serializers.BaseSerializer]:
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "activate":
            return UserActivationSerializer
        return UserSerializer

    def get_permissions(
        self,
    ) -> Iterable[Type[Union[permissions.IsAuthenticated, permissions.AllowAny]]]:
        if self.action == "create" or self.action == "activate":
            self.permission_classes = [permissions.AllowAny]
        elif (
            self.action == "list"
        ):  # For now, there should be a "softer" version of list for authenticated users
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def get_instance(self) -> Union[AbstractBaseUser, AnonymousUser]:
        return self.request.user

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(["post"], detail=False)
    def activate(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_object = serializer.user
            user_object.is_active = True
            user_object.save(update_fields=["is_active"])
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(["get", "post", "put", "patch"], detail=False)
    def me(self, request: Request, *args, **kwargs) -> Response:
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
