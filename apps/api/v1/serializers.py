"""Serializers for the API v1 endpoints."""

from rest_framework import serializers


class ExampleResponseSerializer(serializers.Serializer):
    """Serializer for example API responses."""

    message = serializers.CharField()
    user = serializers.CharField()
    is_superuser = serializers.BooleanField()


class AdminDataSerializer(serializers.Serializer):
    """Serializer for admin-only data responses."""

    message = serializers.CharField()
    user = serializers.CharField()
    admin_secret = serializers.CharField()
    user_count = serializers.IntegerField()
