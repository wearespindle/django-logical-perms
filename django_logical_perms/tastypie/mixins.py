class FieldPermissionsMixin(object):
    """Incorporate per object field-based permissions in Tastypie.

    You can use this class as a mixin in your API or Resource classes
    to allow for compatibility with object field-based permissions in your API.

    Note:
        You must specify ``field_permissions`` in the Meta class.
        You can use ``FieldPermissionsConfigSet`` class for this.
    """
    def update_bundle_fields(self, bundle, action):
        allowed_fields = self.Meta.field_permissions.get_permitted_field_names(
            action=action, user=bundle.request.user, obj=bundle.obj)

        bundle_keys = list(bundle.data.keys())

        for field in bundle_keys:
            if field not in allowed_fields:
                del bundle.data[field]

        return bundle

    def hydrate(self, bundle):
        return super(FieldPermissionsMixin, self).hydrate(
            self.update_bundle_fields(bundle, action='change'))

    def dehydrate(self, bundle):
        return super(FieldPermissionsMixin, self).dehydrate(
            self.update_bundle_fields(bundle, action='view'))
