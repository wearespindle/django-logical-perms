from django.contrib.auth.models import User

from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from django_logical_perms.tastypie.mixins import FieldPermissionsMixin
from ..permissions import UserPermissionConfigSet


class UserAPI(FieldPermissionsMixin, ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'patch']
        limit = 100
        authentication = SessionAuthentication()
        authorization = Authorization()
        field_permissions = UserPermissionConfigSet()
