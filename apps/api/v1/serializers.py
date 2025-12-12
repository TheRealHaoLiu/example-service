"""Serializers for the API v1 endpoints."""

from rest_framework import serializers

from ansible_base.lib.serializers.common import CommonUserSerializer, NamedCommonModelSerializer
from ansible_base.rbac.api.related import RelatedAccessMixin
from apps.core.models import Organization, Team, User


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


class OrganizationSerializer(RelatedAccessMixin, NamedCommonModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class TeamSerializer(RelatedAccessMixin, NamedCommonModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class UserSerializer(CommonUserSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        exclude = ('user_permissions', 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
