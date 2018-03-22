from django_logical_perms.permissions import BaseP


class PermissionStorage(object):
    """The default storage class for logical permissions."""
    def __init__(self):
        self._permissions = {}

    def get_all_permissions(self):
        """Return a list of all currently registered permissions.

        :returns: dict -- A dictionary of all currently registered permissions.
        """
        return self._permissions

    def register(self, permission):
        """Register a permission with the storage instance.

        :param permission: P -- The permission to register. Must be an instance of BaseP.
        :raises: ValueError
        """
        if not isinstance(permission, BaseP):
            raise ValueError(
                'Registering permissions with the PermissionStorage backend is only '
                'allowed for instances of BaseP.')

        if permission.label is None:
            raise ValueError('The permission must have a label.')

        if permission.label in self.get_all_permissions():
            raise ValueError(
                'The permission {} cannot be registered with the {} storage backend '
                'because another permission with the same name already exists.'.format(
                    permission, self.__class__.__name__))

        self._permissions[permission.label] = permission

    def get_permission(self, label):
        """Returns the permission from the storage or raises a ValueError if it was not found.

        :param label: str -- The permission label to get.
        :raises: ValueError
        """
        permission = self.get_all_permissions().get(label)

        if not permission:
            raise ValueError(
                'There is no permission registered with the label {} in the '
                '{} storage backend.'.format(
                    label, self.__class__.__name__))

        return permission


default_storage = PermissionStorage()
