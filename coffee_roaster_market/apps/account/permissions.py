from django.db.models.base import Model
from rest_framework import permissions
from rest_framework.request import Request


class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, _, obj: Model) -> bool:
        user = request.user
        return user.is_staff or obj.pk
