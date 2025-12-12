"""URL configuration for API v1 endpoints."""

from django.urls import include, path

from .router import router
from .viewsets import AuthenticatedExampleView, SuperAdminExampleView

urlpatterns = [
    path("", include(router.urls)),
    path("example/", AuthenticatedExampleView.as_view(), name="authenticated-example"),
    path("admin-example/", SuperAdminExampleView.as_view(), name="superadmin-example"),
]
