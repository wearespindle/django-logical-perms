from django.apps import AppConfig

from django_logical_perms.loaders import load_all_permissions_modules


class DjangoLogicalPermsConfig(AppConfig):
    name = 'django_logical_perms'

    def ready(self):
        load_all_permissions_modules()
