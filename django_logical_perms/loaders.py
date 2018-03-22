from importlib import import_module

from django.apps import apps
from django.conf import settings


def load_all_permissions_modules():
    """Go through all app configs and try loading their permissions module.

    By loading the permissions modules, the permissions will automatically get registered
    with the storage backend. This will automatically enable evaluation through Django's
    has_perms function (if the custom auth backend is loaded).
    """
    from django_logical_perms.apps import DjangoLogicalPermsConfig

    for _, app_config in apps.app_configs.items():
        if isinstance(app_config, DjangoLogicalPermsConfig):
            continue

        load_permissions_module(app_config)


def load_permissions_module(app_config):
    """Loads the permissions module for the given app.

    :param app_config: The app's AppConfig instance.
    """
    try:
        # Import and only process apps with a permissions module
        permissions_module_name = getattr(settings, 'PERMISSIONS_MODULE_NAME', 'permissions')
        permissions_module_path = '%s.%s' % (app_config.name, permissions_module_name)
        permissions_module = import_module(permissions_module_path)

        print("Loaded permissions from %s" % permissions_module.__name__)

    except ImportError:
        # Skip the app if the permissions module does not exist.
        return
