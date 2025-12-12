"""ViewSets and APIViews for the API v1 endpoints."""

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ansible_base.lib.utils.views.ansible_base import AnsibleBaseView
from ansible_base.rbac import permission_registry
from ansible_base.rbac.api.permissions import AnsibleBaseObjectPermissions, AnsibleBaseUserPermissions
from ansible_base.rbac.policies import visible_users

from apps.api.permissions import IsAuthenticatedUser, IsSuperAdmin
from apps.core.models import Organization, Team, User

from .serializers import (
    AdminDataSerializer,
    ExampleResponseSerializer,
    OrganizationSerializer,
    TeamSerializer,
    UserSerializer,
)


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


class BaseViewSet(ModelViewSet, AnsibleBaseView):
    """Base viewset with RBAC filtering."""

    permission_classes = [AnsibleBaseObjectPermissions]

    def filter_queryset(self, qs):
        cls = qs.model
        if permission_registry.is_registered(cls):
            qs = cls.access_qs(self.request.user, queryset=qs)
        return super().filter_queryset(qs)


class OrganizationViewSet(BaseViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class TeamViewSet(BaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AnsibleBaseUserPermissions]

    def filter_queryset(self, qs):
        qs = visible_users(self.request.user, queryset=qs)
        return super(BaseViewSet, self).filter_queryset(qs)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
