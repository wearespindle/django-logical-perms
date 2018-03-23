import uuid
from unittest import TestCase

from django.contrib.auth.models import AnonymousUser, User

from django_logical_perms.configs import FieldPermissionConfig, FieldPermissionConfigSet
from django_logical_perms.permissions import FunctionalP


class FieldPermissionsTestCase(TestCase):
    def _get_valid_config_set_cls(self):
        only_anon_perm = FunctionalP(lambda user, obj=None: isinstance(user, AnonymousUser))

        class ConfigSet(FieldPermissionConfigSet):
            field_config = [
                FieldPermissionConfig(fields=['field_a'], can_view=True, can_change=True),
                FieldPermissionConfig(fields=['field_b'], can_view=only_anon_perm, can_change=False),
            ]

            allow_view = ('field_c',)
            allow_change = ('field_d',)

        return ConfigSet

    def test_field_config_static(self):
        user = AnonymousUser()
        config = FieldPermissionConfig(fields=['field_a'], can_view=False, can_change=True)

        self.assertFalse(config.can_view(user))
        self.assertTrue(config.can_change(user))

    def test_field_config_dynamic(self):
        user = AnonymousUser()

        perm_yes = FunctionalP(lambda user_, obj=None: True)
        perm_no = FunctionalP(lambda user_, obj=None: False)
        config = FieldPermissionConfig(fields=['field_a'], can_view=perm_yes, can_change=perm_no)

        self.assertTrue(config.can_view(user))
        self.assertFalse(config.can_change(user))

    def test_field_config_default(self):
        # By not specifying can_view and/or can_change, they should default to False
        user = AnonymousUser()
        config = FieldPermissionConfig(fields=['field_a'])

        self.assertFalse(config.can_view(user))
        self.assertFalse(config.can_change(user))

    def test_field_config_validation(self):
        # Fields must be a tuple or list
        with self.assertRaises(ValueError):
            FieldPermissionConfig(fields='this is not a list')

        # Fields must specify at least one field
        with self.assertRaises(ValueError):
            FieldPermissionConfig(fields=[])

        # can_view and can_change must be BaseP instance or bool
        with self.assertRaises(ValueError):
            FieldPermissionConfig(fields=['blep'], can_view='this is invalid')

        with self.assertRaises(ValueError):
            FieldPermissionConfig(fields=['blep'], can_change='this is invalid')

        # These are all valid
        perm = FunctionalP(lambda user_, obj=None: True)

        FieldPermissionConfig(fields=('blep',))
        FieldPermissionConfig(fields=['blep'])
        FieldPermissionConfig(fields=['blep'], can_view=True, can_change=False)
        FieldPermissionConfig(fields=['blep'], can_view=perm, can_change=perm)
        FieldPermissionConfig(fields=['blep'], can_view=perm | perm, can_change=perm & perm)

    def test_field_config_set_validation(self):
        # An empty instantiation should fail because we need at least one field in
        # the field_config, allow_view or allow_change properties.
        with self.assertRaises(ValueError):
            FieldPermissionConfigSet()

        # This should raise a ValueError because we defined a dynamic
        # and a static permission for field_a
        with self.assertRaises(ValueError):
            class ConfigSetInvalid(FieldPermissionConfigSet):
                field_config = [FieldPermissionConfig(fields=['field_a'])]
                allow_view = ('field_a',)

            ConfigSetInvalid()

        # The following set is valid
        config = self._get_valid_config_set_cls()()

        # We should at least have view and change actions
        config._validate_action('view')
        config._validate_action('change')

        # Invalid actions should raise ValueErrors
        with self.assertRaises(ValueError):
            config._validate_action('blep')

    def test_field_config_set(self):
        anon_user = AnonymousUser()
        other_user = User.objects.create(username=uuid.uuid4())  # uuid for randomness
        config = self._get_valid_config_set_cls()()

        # Test view permissions
        self.assertEqual(config.get_permitted_field_names('view', anon_user), ['field_c', 'field_a', 'field_b'])
        self.assertEqual(config.get_permitted_field_names('view', other_user), ['field_c', 'field_a'])

        # Test change permissions
        self.assertEqual(config.get_permitted_field_names('change', anon_user), ['field_d', 'field_a'])
        self.assertEqual(config.get_permitted_field_names('change', other_user), ['field_d', 'field_a'])

        # Now check through is_permitted_field
        self.assertTrue(config.is_permitted_field('view', 'field_b', anon_user))
        self.assertTrue(config.is_permitted_field('view', 'field_c', anon_user))
        self.assertFalse(config.is_permitted_field('view', 'field_b', other_user))
        self.assertTrue(config.is_permitted_field('view', 'field_c', other_user))

        # If the field is not specified it should not be viewable or changeable
        self.assertFalse(config.is_permitted_field('view', 'field_z', anon_user))
        self.assertFalse(config.is_permitted_field('view', 'field_z', other_user))
