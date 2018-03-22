from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from django_logical_perms.decorators import permission
from django_logical_perms.permissions import P, FunctionalP, BaseP
from django_logical_perms.storages import default_storage, PermissionStorage

from tests.permissions import SimplePermission, ChangingPermission, StaticLabelPermission, simple_decorated_permission, \
    simple_labeled_permission, registered_permission


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

    def test_method_based_permission(self):
        # We should be able to create permissions using lambdas through FunctionalP.
        user = AnonymousUser()
        lambda_perm = FunctionalP(lambda user_, obj=None: True)

        self.assertTrue(lambda_perm(user))
        self.assertEqual(lambda_perm.label, 'tests.<lambda>')

        # We should also be able to create permissions with named methods through FunctionalP.
        def can_have_tests_passed(user, obj=None):
            return True

        named_perm = FunctionalP(can_have_tests_passed)

        self.assertTrue(named_perm(user))
        self.assertEqual(named_perm.label, 'tests.can_have_tests_passed')

    def test_storage(self):
        storage = PermissionStorage()

        # There should be nothing in the storage now.
        self.assertEqual(storage.get_all_permissions(), {})

        # We should only be allowed to register BaseP instances with the storage backend.
        with self.assertRaises(ValueError):
            storage.register(object())

        # The BaseP instance must have a label in order for it to be registered with the storage backend.
        with self.assertRaises(ValueError):
            storage.register(BaseP())

        # There should not be a 'demo' permission in the storage now.
        with self.assertRaises(ValueError):
            storage.get_permission('demo')

        # This registration should go as planned.
        permission = FunctionalP(lambda user, obj=None: True, label='demo')
        storage.register(permission)

        self.assertEqual(storage.get_all_permissions(), {'demo': permission})
        self.assertEqual(storage.get_permission('demo'), permission)

        # Should not be able to re-register this permission now.
        with self.assertRaises(ValueError):
            storage.register(permission)

    def test_decorated_permission(self):
        user = AnonymousUser()

        # The permission decorator simply turns a function into a FunctionalP instance.
        self.assertIsInstance(simple_decorated_permission, FunctionalP)
        self.assertTrue(simple_decorated_permission(user))

        # The label should also be set
        self.assertEqual(simple_decorated_permission.label, 'tests.simple_decorated_permission')
        self.assertEqual(repr(simple_decorated_permission), 'P(tests.simple_decorated_permission)')

        # Permissions can also pass in keyword arguments to the decorator.
        self.assertIsInstance(simple_labeled_permission, FunctionalP)
        self.assertTrue(simple_labeled_permission(user))

        # Check for the custom label
        self.assertEqual(simple_labeled_permission.label, 'tests.simple_labeled_permission_custom')
        self.assertEqual(repr(simple_labeled_permission), 'P(tests.simple_labeled_permission_custom)')

        # We can also register the permission directly with the default storage
        # by way of the decorator.
        self.assertEqual(registered_permission.label, 'tests.registered_permission')
        self.assertEqual(repr(registered_permission), 'P(tests.registered_permission)')
        self.assertEqual(default_storage.get_permission('tests.registered_permission'), registered_permission)
        self.assertTrue(registered_permission(user))
        self.assertTrue(default_storage.get_permission('tests.registered_permission')(user))

        # We should not be able to decorate a non-callable
        with self.assertRaises(ValueError):
            permission('blep')
