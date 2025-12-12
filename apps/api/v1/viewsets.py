"""ViewSets and APIViews for the API v1 endpoints."""

from django.contrib.auth import get_user_model
from rest_framework.response import Response

from ansible_base.lib.utils.views.ansible_base import AnsibleBaseView

from apps.api.permissions import IsAuthenticatedUser, IsSuperAdmin

from .serializers import AdminDataSerializer, ExampleResponseSerializer


class AuthenticatedExampleView(AnsibleBaseView):
    """
    Example API endpoint accessible by any authenticated user.

    Returns a greeting message with user information.
    """

    permission_classes = [IsAuthenticatedUser]

    def get(self, request):
        """Return a greeting for authenticated users."""
        data = {
            "message": "Hello, authenticated user!",
            "user": request.user.username,
            "is_superuser": request.user.is_superuser,
        }
        serializer = ExampleResponseSerializer(data)
        return Response(serializer.data)


class SuperAdminExampleView(AnsibleBaseView):
    """
    Example API endpoint accessible only by superadmin users.

    Returns admin-only data including sensitive information.
    """

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        """Return admin-only data for superusers."""
        UserModel = get_user_model()
        data = {
            "message": "Welcome, superadmin!",
            "user": request.user.username,
            "admin_secret": "This is sensitive admin-only data",
            "user_count": UserModel.objects.count(),
        }
        serializer = AdminDataSerializer(data)
        return Response(serializer.data)
