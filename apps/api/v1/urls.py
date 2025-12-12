"""URL configuration for API v1 endpoints."""

from django.urls import path

from .viewsets import AuthenticatedExampleView, SuperAdminExampleView

urlpatterns = [
    path("example/", AuthenticatedExampleView.as_view(), name="authenticated-example"),
    path("admin-example/", SuperAdminExampleView.as_view(), name="superadmin-example"),
]
