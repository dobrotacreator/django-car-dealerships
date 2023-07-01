from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has admin privileges
        return request.user.is_superuser


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the associated object
        return request.user == obj.user


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for all users
        return request.method in SAFE_METHODS
