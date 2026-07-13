from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем курса или урока."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
