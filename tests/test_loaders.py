from django.test import TestCase

from django_logical_perms.loaders import load_all_permissions_modules


class PermissionLoaderTestCase(TestCase):
    def test_permission_loader(self):
        loaded_apps = [
            app_config.name
            for app_config, success
            in load_all_permissions_modules(yield_loads=True)
            if success]

        self.assertEqual(loaded_apps, ['tests', 'tests.api'])

    def test_permission_loader_without_yield(self):
        # The loader shouldn't yield any results if we don't
        # explicitly set the yield_loads parameter.
        loaded_apps = [x for x in load_all_permissions_modules()]
        self.assertEqual(loaded_apps, [])
