from rest_framework import permissions


class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, _, obj):
        user = request.user
        return user.is_staff or obj.pk
