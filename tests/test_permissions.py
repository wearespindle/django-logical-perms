import uuid

from django.contrib.auth.models import AnonymousUser, Permission, User
from django.test import TestCase
from django_logical_perms.backends import LogicalPermissionsBackend
from django_logical_perms.decorators import permission
from django_logical_perms.exceptions import PermissionNotFound
from django_logical_perms.permissions import (
    BaseLogicalPermission,
    FunctionalLogicalPermission,
    has_perm,
    LogicalPermission,
)
from django_logical_perms.storages import default_storage, PermissionStorage

from .permissions import (
    ChangingPermission,
    registered_permission,
    simple_decorated_permission,
    simple_labeled_permission,
    SimplePermission,
    StaticLabelPermission,
)


class PermissionsTestCase(TestCase):
    def test_not_implemented_permission(self):
        p_instance = LogicalPermission()
        user = AnonymousUser()

        evaluators = (
            p_instance.has_permission,
            p_instance.test,
            p_instance,
        )

        # LogicalPermission must be subclassed. If not, it
        # should raise NotImplementedError.
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

        # Simply calling a LogicalPermission instance should evaluate
        # the permission.
        for fn in evaluators:
            self.assertTrue(fn(user))
            self.assertTrue(fn(user, obj=simple_perm))

    def test_permission_cache(self):
        random_perm = ChangingPermission()
        user = AnonymousUser()

        # Set up some predictable outputs.
        random_perm.set_result('a', True)
        random_perm.set_result('b', False)

        # If we evaluate 'a' and 'b', they should match the results we set.
        self.assertTrue(random_perm(user, obj='a'))
        self.assertFalse(random_perm(user, obj='b'))

        # Change the results. The permissions should still evaluate to the old
        # results as they're being cached on the AnonymousUser object.
        random_perm.set_result('a', False)
        random_perm.set_result('b', True)

        # If we evaluate 'a' and 'b', they should match the old results.
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

        # Default label format is '{app_name}.{permission_name}'.
        self.assertEqual(simple_perm.label, 'tests.SimplePermission')
        self.assertEqual(random_perm.label, 'tests.ChangingPermission')
        self.assertEqual(static_label_perm.label, 'tests.static_permission')

        # The labels should be in the representations also.
        self.assertEqual(repr(simple_perm), 'LogicalPermission(tests.SimplePermission)')
        self.assertEqual(repr(random_perm), 'LogicalPermission(tests.ChangingPermission)')
        self.assertEqual(repr(static_label_perm), 'LogicalPermission(tests.static_permission)')

    def test_method_based_permission(self):
        # We should be able to create permissions using lambdas
        # through FunctionalLogicalPermission.
        user = AnonymousUser()
        lambda_perm = FunctionalLogicalPermission(lambda user_, obj=None: True)

        self.assertTrue(lambda_perm(user))
        self.assertEqual(lambda_perm.label, 'tests.<lambda>')

        # We should also be able to create permissions with named
        # methods through FunctionalLogicalPermission.
        def can_have_tests_passed(user, obj=None):
            return True

        named_perm = FunctionalLogicalPermission(can_have_tests_passed)

        self.assertTrue(named_perm(user))
        self.assertEqual(named_perm.label, 'tests.can_have_tests_passed')

    def test_storage(self):
        storage = PermissionStorage()

        # There should be nothing in the storage now.
        self.assertEqual(storage.get_all_permissions(), {})

        # We should only be allowed to register BaseLogicalPermission instances
        # with the storage backend.
        with self.assertRaises(ValueError):
            storage.register(object())

        # The BaseLogicalPermission instance must have a label in order for it to
        # be registered with the storage backend.
        with self.assertRaises(ValueError):
            storage.register(BaseLogicalPermission())

        # There should not be a 'demo' permission in the storage now.
        with self.assertRaises(PermissionNotFound):
            storage.get_permission('demo')

        # This registration should go as planned.
        perm = FunctionalLogicalPermission(lambda user, obj=None: True, label='demo')
        storage.register(perm)

        self.assertEqual(storage.get_all_permissions(), {'demo': perm})
        self.assertEqual(storage.get_permission('demo'), perm)

        # Should not be able to re-register this permission now.
        with self.assertRaises(ValueError):
            storage.register(perm)

        # Ability to register a permission with a custom label.
        storage.register(perm, label='blep')

        self.assertEqual(storage.get_all_permissions(), {'demo': perm, 'blep': perm})
        self.assertEqual(storage.get_permission('blep'), perm)

        # Should not be able to re-register this permission now.
        with self.assertRaises(ValueError):
            storage.register(perm, label='blep')

    def test_decorated_permission(self):
        user = AnonymousUser()

        # The permission decorator simply turns a function into
        # a FunctionalLogicalPermission instance.
        self.assertIsInstance(simple_decorated_permission, FunctionalLogicalPermission)
        self.assertTrue(simple_decorated_permission(user))

        # The label should also be set.
        self.assertEqual(simple_decorated_permission.label, 'tests.simple_decorated_permission')
        self.assertEqual(repr(simple_decorated_permission), 'LogicalPermission(tests.simple_decorated_permission)')

        # Permissions can also pass in keyword arguments to the decorator.
        self.assertIsInstance(simple_labeled_permission, FunctionalLogicalPermission)
        self.assertTrue(simple_labeled_permission(user))

        # Check for the custom label.
        self.assertEqual(simple_labeled_permission.label, 'tests.simple_labeled_permission_custom')
        self.assertEqual(repr(simple_labeled_permission), 'LogicalPermission(tests.simple_labeled_permission_custom)')

        # We can also register the permission directly with the default storage
        # by way of the decorator.
        self.assertEqual(registered_permission.label, 'tests.registered_permission')
        self.assertEqual(repr(registered_permission), 'LogicalPermission(tests.registered_permission)')
        self.assertEqual(default_storage.get_permission('tests.registered_permission'), registered_permission)
        self.assertTrue(registered_permission(user))
        self.assertTrue(default_storage.get_permission('tests.registered_permission')(user))

        # We should not be able to decorate a non-callable.
        with self.assertRaises(ValueError):
            permission('blep')

    def test_django_integration(self):
        user = AnonymousUser()

        # Should work with class-based permissions.
        class ClassPermission(LogicalPermission):
            def has_permission(self, user, obj=None):
                return True

        default_storage.register(ClassPermission())

        self.assertTrue(user.has_perm('tests.ClassPermission'))
        self.assertFalse(user.has_perm('tests.blep'))

        # Should work with decorated permissions.
        @permission(register=True)
        def inline_decorated(user, obj=None):
            return True

        self.assertTrue(user.has_perm('tests.inline_decorated'))
        self.assertFalse(user.has_perm('tests.blep'))

        # Should work with custom labeled permissions.
        default_storage.register(ClassPermission(), label='tests.blep')
        self.assertTrue(user.has_perm('tests.blep'))

        # Should work with the permission registration from
        # the app's permissions.py.
        self.assertTrue(user.has_perm('tests.registered_permission'))

        # The authenticate method should just return None,
        # we don't authenticate users.
        self.assertIsNone(LogicalPermissionsBackend().authenticate())

    def test_processed_permissions(self):
        user = AnonymousUser()
        yes = True
        no = False

        @permission
        def perm_yes(user, obj=None):
            return yes

        @permission
        def perm_no(user, obj=None):
            return no

        # Invert.
        self.assertFalse((~perm_yes)(user))
        self.assertIsNone((~perm_yes).label)
        self.assertEqual(repr(~perm_no), 'Not<LogicalPermission(tests.perm_no)>')

        # Or.
        self.assertTrue((perm_yes | perm_no)(user))
        self.assertIsNone((perm_yes | perm_no).label)
        self.assertEqual(repr(perm_yes | perm_no), 'Or<LogicalPermission(tests.perm_yes), LogicalPermission(tests.perm_no)>')

        # And.
        self.assertFalse((perm_yes & perm_no)(user))
        self.assertIsNone((perm_yes & perm_no).label)
        self.assertEqual(repr(perm_yes & perm_no), 'And<LogicalPermission(tests.perm_yes), LogicalPermission(tests.perm_no)>')

        # Xor.
        self.assertTrue((perm_yes ^ perm_no)(user))
        self.assertFalse((perm_yes ^ perm_yes)(user))
        self.assertTrue((perm_no ^ perm_yes)(user))

        self.assertIsNone((perm_yes ^ perm_no).label)
        self.assertEqual(repr(perm_yes ^ perm_no), 'Xor<LogicalPermission(tests.perm_yes), LogicalPermission(tests.perm_no)>')

        # Individual permissions get cached. If we change their output,
        # the chained permissions should still evaluate to the same result
        # through cache.
        perm = perm_yes & perm_no

        # No changes.
        self.assertTrue(perm_yes(user))
        self.assertFalse(perm_no(user))
        self.assertFalse(perm(user))

        # Now change the permission output.
        no = True

        self.assertTrue(perm_yes(user))
        self.assertFalse(perm_no(user))
        self.assertFalse(perm(user))

        # Re-fetch the user. This should clear the cache.
        user = AnonymousUser()

        self.assertTrue(perm_yes(user))
        self.assertTrue(perm_no(user))
        self.assertTrue(perm(user))

    def test_builtin_permissions(self):
        # We will need an actual user for this. We'll use uuid
        # as username as it's random enough.
        user = User.objects.create(username=uuid.uuid4())
        target_perm = Permission.objects.all().last()
        codename = '%s.%s' % (target_perm.content_type.app_label, target_perm.codename)

        # Create new instance of the `has_perm` permission.
        user_has_random_permission = has_perm(codename)

        self.assertFalse(user.has_perm(codename))
        self.assertFalse(user_has_random_permission(user))

        # Now add the permission to the user.
        user.user_permissions.add(target_perm)

        # Re-fetch the user to invalidate cache.
        user = User.objects.get(id=user.id)

        self.assertTrue(user.has_perm(codename))
        self.assertTrue(user_has_random_permission(user))
