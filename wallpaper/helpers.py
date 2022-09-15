from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnerPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_staff or request.method in SAFE_METHODS:
            return True
        return False
