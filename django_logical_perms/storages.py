from .exceptions import PermissionNotFound
from .permissions import BaseLogicalPermission


class PermissionStorage(object):
    """
    The default storage class for logical permissions.
    """
    def __init__(self):
        self._permissions = {}

    def get_all_permissions(self):
        """
        Return a list of all currently registered permissions.

        Returns:
            dict: A dictionary of all currently registered permissions.
        """
        return self._permissions

    def register(self, permission, label=None):
        """
        Register a permission with the storage instance.

        Note:
            The ``label`` param will always prioritize over the permission
            instance label. If you do not explicitly specify a label, the
            permission's label will be used (``permission.label``).

        Args:
            permission (BaseLogicalPermission): The permission to register.
            label (str): An optional custom label for the permission.

        Raises:
            ValueError: If the permission is not an instance of
                :class:`BaseLogicalPermission`.
        """
        if not isinstance(permission, BaseLogicalPermission):
            raise ValueError(
                'Registering permissions with the PermissionStorage backend is only '
                'allowed for instances of BaseLogicalPermission.')

        if label is None:
            label = permission.label

        if label is None:
            raise ValueError('The permission must have a label.')

        if label in self.get_all_permissions():
            raise ValueError(
                'The permission {} ({}) cannot be registered with the {} storage backend '
                'because another permission with the same name already exists.'.format(
                    label, permission, self.__class__.__name__))

        self._permissions[label] = permission

    def get_permission(self, label):
        """
        Returns the permission from the storage.

        This function will always return the permission instance from the
        storage. If the permission is not found it will raise a
        :class:`PermissionNotFound` exception.

        Args:
            label (str): The permission's label.

        Raises:
            PermissionNotFound: If the permission was not found.

        Returns:
            BaseLogicalPermission: The permission from the storage.
        """
        permission = self.get_all_permissions().get(label, None)

        if permission is None:
            raise PermissionNotFound(
                'There is no permission registered with the label {} in the '
                '{} storage backend.'.format(
                    label, self.__class__.__name__))

        return permission


default_storage = PermissionStorage()
