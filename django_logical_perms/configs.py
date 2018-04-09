from django_logical_perms.permissions import BaseLogicalPermission


class FieldPermissionConfig(object):
    """
    Define permissions for a specific field of an object.
    """

    def __init__(self, fields, can_view=None, can_change=None):
        """
        Define permissions for a specific field of an object.

        You must define one or more fields that the permission applies to.
        You can leave ``can_view`` and ``can_change`` so that they will
        default to False.

        Note:
            If you use ``FieldPermissionConfigSet`` and specified a static
            list of allowed fields (view or change), the static list will
            take priority over the FieldPermissionConfig instance.

        Args:
            fields (tuple, list): Fields these permissions apply to.
            can_view (bool, BaseLogicalPermission): Either a static boolean or
                a BaseLogicalPermission instance.
            can_change (bool, BaseLogicalPermission): Either a static boolean or
                a BaseLogicalPermission instance.
        """
        if not isinstance(fields, tuple) and not isinstance(fields, list):
            raise ValueError('`fields` must be a tuple or list.')

        if len(fields) == 0:
            raise ValueError('`fields` must specify at least one field.')

        if can_view is not None and not isinstance(can_view, (BaseLogicalPermission, bool)):
            raise ValueError('`can_view` must be an instance of BaseLogicalPermission or a bool.')

        if can_change is not None and not isinstance(can_change, (BaseLogicalPermission, bool)):
            raise ValueError('`can_change` must be an instance of BaseLogicalPermission or a bool.')

        self.fields = fields

        self._can_view_perm = can_view or False
        self._can_change_perm = can_change or False

    def _check_perm(self, perm, user, obj):
        """
        Check permission for the given user and object.

        Args:
            perm (bool, BaseLogicalPermission): The permission to check against.
            obj (object): The object to pass into the permission evaluator.
            user (User): A User instance to check the permission against.

        Returns:
            bool: True if the permission was granted.
        """
        if isinstance(perm, BaseLogicalPermission):
            return perm(user, obj)

        return perm

    def can_change(self, user, obj=None):
        """
        Check change permission for the given user and optional object.

        Args:
            user (User): A User instance to check the permission against.
            obj (object): An optional object to check the permission against.

        Returns:
            bool: True if the user can change the field on the object.
        """
        return self._check_perm(self._can_change_perm, user, obj)

    def can_view(self, user, obj=None):
        """
        Check view permission for the given user and optional object.

        Args:
            user (User): A User instance to check the permission against.
            obj (object): An optional object to check the permission against.

        Returns:
            bool: True if the user is allowed to view the object field.
        """
        return self._check_perm(self._can_view_perm, user, obj)


class FieldPermissionConfigSet(object):
    """
    Define permissions using a set of ``FieldPermissionConfig`` instances.

    Note:
        Statically allowed fields get priority over dynamically configured
        permissions. There is no use in defining a field a static and dynamic
        permission.
    """
    ACTIONS = ('view', 'change',)

    field_config = []
    allow_view = []
    allow_change = []

    def __init__(self):
        if len(self.field_config) + len(self.allow_view) + len(self.allow_change) == 0:
            raise ValueError('Expected at least one field config or one static config.')

        for config in self.field_config:
            for field in config.fields:
                if field in self.allow_view or field in self.allow_change:
                    raise ValueError(
                        'The field {} was specified with a dynamic and static permission. '
                        'You must remove the permission from the list of static permissions '
                        'or incorporate your static permissions into the dynamic config. '
                        'It is not supported to have a field have both a static and '
                        'dynamic permission config.')

    def _validate_action(self, action):
        """
        Validates whether the action string is valid.

        Args:
            action (str): Action string to validate.

        Raises:
            ValueError
        """
        if action not in self.ACTIONS:
            raise ValueError('Only change and view are supported actions.')

    def _iterate_permitted_field_names(self, action, user, obj=None):
        """
        Iterates over all permitted fields.

        Args:
            action (str): Action to check permission against.
            user (User): A User instance to check the permission against.
            obj (object): An optional object to check the permission against.
        """
        # First iterate over all the statically allowed fields.
        for field_name in getattr(self, 'allow_{}'.format(action)):
            yield field_name

        # Now iterate over the dynamically allowed fields.
        for config in self.field_config:
            if getattr(config, 'can_{}'.format(action))(user, obj):
                for field_name in config.fields:
                    yield field_name

    def get_permitted_field_names(self, action, user, obj=None):
        """
        Get a list of all permitted fields.

        Args:
            action (str): Action to check permission against.
            user (User): A User instance to check the permission against.
            obj (object): An optional object to check against.

        Returns:
            list: List of permitted fields for the given action, user
            and optional object.
        """
        self._validate_action(action)
        return [field_name for field_name in self._iterate_permitted_field_names(action, user, obj)]

    def is_permitted_field(self, action, field_name, user, obj=None):
        """
        Check if the given action is permitted for the user.

        Args:
            action (str): Action to check against.
            field_name (str): The field name to check against.
            user (User): A User instance to check against.
            obj (object): An optional object to check against

        Returns:
            bool: True if the user is allowed the action on the specified field
            of the optional object.
        """
        self._validate_action(action)

        # Short circuit.
        if field_name in getattr(self, 'allow_{}'.format(action), []):
            return True

        # Get the field's config and permissions.
        for config in self.field_config:
            if field_name in config.fields:
                return getattr(config, 'can_{}'.format(action))(user, obj)

        # Field is not defined, do not allow.
        return False
