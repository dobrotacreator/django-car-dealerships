from rest_framework.permissions import BasePermission

from src.authorization.models import User


class IsDealership(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.DEALERSHIP
