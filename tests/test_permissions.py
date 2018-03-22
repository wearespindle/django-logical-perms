from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from tests.permissions import SimplePermission, ChangingPermission


class PermissionsTestCase(TestCase):
    def test_permission(self):
        simple_perm = SimplePermission()
        user = AnonymousUser()

        # Simply calling a P instance should evaluate the permission
        self.assertTrue(simple_perm(user))
        self.assertTrue(simple_perm(user, obj=simple_perm))

    def test_permission_cache(self):
        random_perm = ChangingPermission()
        user = AnonymousUser()

        # Set up some predictable outputs
        random_perm.set_result('a', True)
        random_perm.set_result('b', False)

        # If we evaluate 'a' and 'b', they should match the results we set
        self.assertTrue(random_perm(user, obj='a'))
        self.assertFalse(random_perm(user, obj='b'))

        # Change the results. The permissions should still evaluate to the old
        # results as they're being cached on the AnonymousUser object.
        random_perm.set_result('a', False)
        random_perm.set_result('b', True)

        # If we evaluate 'a' and 'b', they should match the old results
        self.assertTrue(random_perm(user, obj='a'))
        self.assertFalse(random_perm(user, obj='b'))

        # Re-fetch the user. This should clear its cache.
        user = AnonymousUser()

        # If we evaluate 'a' and 'b', they should match the new results because of
        # the new, empty cache.
        self.assertFalse(random_perm(user, obj='a'))
        self.assertTrue(random_perm(user, obj='b'))

    def test_permission_repr(self):
        simple_perm = SimplePermission()
        random_perm = ChangingPermission()

        # Default representation format is '{app_name}.{permission_name}'
        self.assertEqual(repr(simple_perm), "P(tests.SimplePermission)")
        self.assertEqual(repr(random_perm), "P(tests.ChangingPermission)")
