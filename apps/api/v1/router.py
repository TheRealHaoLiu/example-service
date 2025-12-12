"""Router configuration for API v1 endpoints."""

from ansible_base.lib.routers import AssociationResourceRouter
from . import viewsets

router = AssociationResourceRouter()

router.register(
    r'organizations',
    viewsets.OrganizationViewSet,
    related_views={
        'teams': (viewsets.TeamViewSet, 'teams'),
    },
)

router.register(
    r'teams',
    viewsets.TeamViewSet,
    related_views={
        'organization': (viewsets.OrganizationViewSet, 'organization'),
    },
)

router.register(
    r'users',
    viewsets.UserViewSet,
    basename='user',
)
