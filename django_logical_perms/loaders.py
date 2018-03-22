from importlib import import_module

from django.apps import apps
from django.conf import settings


def load_all_permissions_modules():
    for _, app_config in apps.app_configs.items():
        load_permissions_module(app_config)


def load_permissions_module(app_config):
    try:
        # Import and only process apps with a permissions module
        permissions_module_name = getattr(settings, 'PERMISSIONS_MODULE_NAME', 'permissions')
        permissions_module_path = '%s.%s' % (app_config.name, permissions_module_name)
        permissions_module = import_module(permissions_module_path)

        print("Loaded permissions from %s" % permissions_module.__name__)

    except ImportError:
        # Skip the app if the permissions module does not exist.
        return
