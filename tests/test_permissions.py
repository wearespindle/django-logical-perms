from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from django_logical_perms.permissions import P

from tests.permissions import SimplePermission, ChangingPermission, StaticLabelPermission


class PermissionsTestCase(TestCase):
    def test_not_implemented_permission(self):
        p_instance = P()
        user = AnonymousUser()

        evaluators = (
            p_instance.has_permission,
            p_instance.test,
            p_instance,
        )

        # P must be subclassed. If not, it should raise NotImplementedError.
        for fn in evaluators:
            with self.assertRaises(NotImplementedError):
                fn(user)

    def test_permission(self):
        simple_perm = SimplePermission()
        user = AnonymousUser()

        evaluators = (
            simple_perm.has_permission,
            simple_perm.test,
            simple_perm,
        )

        # Simply calling a P instance should evaluate the permission
        for fn in evaluators:
            self.assertTrue(fn(user))
            self.assertTrue(fn(user, obj=simple_perm))

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

    def test_permission_label(self):
        simple_perm = SimplePermission()
        random_perm = ChangingPermission()
        static_label_perm = StaticLabelPermission()

        # Default label format is '{app_name}.{permission_name}'
        self.assertEqual(simple_perm.label, 'tests.SimplePermission')
        self.assertEqual(random_perm.label, 'tests.ChangingPermission')
        self.assertEqual(static_label_perm.label, 'tests.static_permission')

        # The labels should be in the representations also
        self.assertEqual(repr(simple_perm), 'P(tests.SimplePermission)')
        self.assertEqual(repr(random_perm), 'P(tests.ChangingPermission)')
        self.assertEqual(repr(static_label_perm), 'P(tests.static_permission)')
