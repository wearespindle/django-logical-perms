from django.contrib.auth.models import User
from django_logical_perms.rest_framework import serializers

from ..permissions import UserPermissionConfigSet


class UserSerializer(serializers.FieldPermissionsSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)
        field_permissions = UserPermissionConfigSet()
