from rest_framework.permissions import BasePermission

from src.authorization.models import User


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.CUSTOMER
