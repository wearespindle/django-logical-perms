from django.core.exceptions import PermissionDenied

from django_logical_perms.exceptions import PermissionNotFound
from django_logical_perms.storages import default_storage


class LogicalPermissionsBackend(object):
    """
    A Django auth-compatible backend for checking permissions.
    """

    def authenticate(self, *args, **kwargs):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check whether a user has a given permission on an optional object.

        Please note that this backend will use the default callable
        implementation of the permission. This normally would invoke the
        ``test`` method on those permissions - which also does caching.

        In order to clear the cache you must re-fetch the User instance,
        just as with the default Django permissions.

        Args:
            user_obj (User): The Django User to evaluate the permission on.
            perm (str): The label of the permission. Should be registered
                in default_storage.
            obj: Optional object to do object-level permission checks.

        Returns:
            bool: True if the user was granted the permission.

        Raises:
            PermissionDenied: Short-circuits the permission evaluation if
                the permission was explicitly denied.
        """
        try:
            # Fetch the permission from the default storage.
            permission = default_storage.get_permission(perm)

            if not permission(user_obj, obj):
                raise PermissionDenied()

            return True

        except PermissionNotFound:
            return False
