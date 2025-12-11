"""Custom permission classes for the API app."""

from rest_framework.permissions import BasePermission, IsAuthenticated


class IsSuperAdmin(BasePermission):
    """
    Permission class that only allows superadmin (superuser) access.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsAuthenticatedUser(IsAuthenticated):
    """
    Permission class that allows any authenticated user.
    This is an alias for IsAuthenticated for clarity.
    """

    pass
