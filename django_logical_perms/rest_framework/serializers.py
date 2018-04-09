from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from django_logical_perms.configs import FieldPermissionConfigSet


class FieldPermissionsSerializer(serializers.ModelSerializer):
    """
    Incorporate per object field-based permissions in REST framework.

    You can use this class as your serializer (or extend it) to have
    field-based permissions being evaluated on every object that's
    getting serialized.

    Note:
        You must specify ``field_permissions`` in the Meta class.
        You can use ``FieldPermissionsConfigSet`` class for this.
    """
    def __init__(self, *args, **kwargs):
        if not hasattr(self.Meta, 'field_permissions'):
            raise ValueError(
                'You must specify the `field_permissions` setting in your Meta class in order '
                'to use the FieldPermissionSerializer.')

        if not isinstance(self.Meta.field_permissions, FieldPermissionConfigSet):
            raise ValueError(
                'The specified field permissions config must be an instance of the '
                '`FieldPermissionsConfigSet` class.')

        super(FieldPermissionsSerializer, self).__init__(*args, **kwargs)

    def _get_request(self):
        request = self.context.get('request', None)

        if request is None:
            raise ValueError(
                '`request` must be passed into the serializer context '
                'in order to use FieldPermissionsSerializer.')

        return request

    def to_representation(self, instance):
        request = self._get_request()
        fields = self._readable_fields
        ret = OrderedDict()

        # Get fields that the user is allowed to view.
        allowed_fields = self.Meta.field_permissions.get_permitted_field_names(
            action='view', obj=instance, user=request.user)

        # Skip fields that the user is not allowed to view. Use the SkipField
        # exception because `field.get_attribute` can also raise that.
        for field in fields:
            try:
                if field.field_name not in allowed_fields:
                    raise SkipField()

                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # Filter related objects that are None as we don't have to serialize
            # them.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            ret[field.field_name] = None if check_for_none is None else field.to_representation(attribute)

        return ret

    def is_valid(self, raise_exception=False):
        # Initial data must be set in order to determine the fields to be
        # updated.
        if not hasattr(self, 'initial_data'):
            raise ValueError(
                'Cannot call `.is_valid()` as no `data=` keyword argument was '
                'passed when instantiating the serializer instance.')

        request = self._get_request()
        disallowed_fields = []

        # Determine fields that cannot be changed.
        for field_name, field_val in self.initial_data.items():
            permit_changes = self.Meta.field_permissions.is_permitted_field(
                action='change', field_name=field_name, obj=self.instance, user=request.user)

            if not permit_changes:
                disallowed_fields.append(field_name)

        # Delete the fields from the initial data set - we can't do it inside
        # the for loop as it will update the dict that we're iterating on.
        for field_name in disallowed_fields:
            del self.initial_data[field_name]

        return super(FieldPermissionsSerializer, self).is_valid(raise_exception=raise_exception)
