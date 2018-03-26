from django.conf import settings

from django_logical_perms.permissions import FunctionalP
from django_logical_perms.storages import default_storage


def permission(func=None, label=None, register=None):
    """Decorator for turning an ordinary function into a permission.

    :param func: The permission evaluator.
    :param label: Optional label for the permission. If it's not set, a
                  label will automatically be generated for the permission.
    :param register: Optional, whether to automatically register the permission
                     with the authentication backend. If it's not set, the
                     default settings will be used.
    """

    def actual_decorator(func_):
        # The thing that we're decorating should at least be a callable.
        if not callable(func_):
            raise ValueError(
                'The permission decorator can only be used on callables. '
                'Did you set a label without explicitly specifying the '
                '`label` keyword argument?')

        # Create the actual permission object
        p = FunctionalP(check_func=func_, label=label)

        # Register with the default storage if specified
        if register is True:
            default_storage.register(p)

        return p

    # Default to global settings if register is None
    if register is None:
        register = getattr(settings, 'PERMISSIONS_DEFAULT_REGISTER_WITH_BACKEND', False)

    # `func` will only be set if the user used the decorator without passing
    # in keyword arguments. In that case we should pass in the function to the
    # actual decorator.
    if func is not None:
        return actual_decorator(func)

    return actual_decorator
