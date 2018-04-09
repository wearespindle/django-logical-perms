from django.conf import settings

from django_logical_perms.permissions import FunctionalP
from django_logical_perms.storages import default_storage

from functools import partial, wraps


def permission(func=None, label=None, register=None):
    """Decorator for turning an ordinary function into a permission.

    :param func: The permission evaluator.
    :param label: Optional label for the permission. If it's not set, a
                  label will automatically be generated for the permission.
    :param register: Optional, whether to automatically register the permission
                     with the authentication backend. If it's not set, the
                     default settings will be used.
    """
    if func is None:
        return partial(permission, label=label, register=register)

    # The thing that we're decorating should at least be a callable.
    if not callable(func):
        raise ValueError(
            'The permission decorator can only be used on callables. '
            'Did you set a label without explicitly specifying the '
            '`label` keyword argument?')

    # Default to global settings if register is None
    if register is None:
        register = getattr(settings, 'PERMISSIONS_DEFAULT_REGISTER_WITH_BACKEND', False)

    @wraps(func)
    def actual_decorator():
        # Create the actual permission object
        instance = FunctionalP(check_func=func, label=label)

        # Register with the default storage if specified
        if register is True:
            default_storage.register(instance)

        return instance

    return actual_decorator()
