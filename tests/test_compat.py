import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django_logical_perms.rest_framework.serializers import FieldPermissionsSerializer
from tests.api.rest_framework.serializers import UserSerializer


class RestFrameworkTestCase(TestCase):
    def setUp(self):
        # Create some random users
        User.objects.create_user(username='user1', password='user1', email='user1@localhost', is_staff=True)
        User.objects.create_user(username='user2', password='user2', email='user2@localhost')
        User.objects.create_user(username='user3', password='user3', email='user3@localhost')

    def test_serializer_validators(self):
        # This should fail because Meta.field_permissions is required but was not defined
        with self.assertRaises(ValueError):
            class InvalidSerializer(FieldPermissionsSerializer):
                class Meta:
                    model = User

            InvalidSerializer()

        # This should fail because Meta.field_permissions is not an instance of FieldPermissionConfigSet
        with self.assertRaises(ValueError):
            class InvalidSerializer(FieldPermissionsSerializer):
                class Meta:
                    model = User
                    field_permissions = []

            InvalidSerializer()

        # This should be instantiated without any problems
        UserSerializer()

        # This should raise ValueError again because no initial data was passed in
        with self.assertRaises(ValueError):
            UserSerializer().is_valid()

    def _test_always_visible_fields(self, resp):
        # IDs should be visible
        self.assertTrue('id' in resp.data[0])
        self.assertTrue('id' in resp.data[1])
        self.assertTrue('id' in resp.data[2])

        # Usernames should be visible
        self.assertTrue('username' in resp.data[0])
        self.assertTrue('username' in resp.data[1])
        self.assertTrue('username' in resp.data[2])

        # First names should be visible
        self.assertTrue('first_name' in resp.data[0])
        self.assertTrue('first_name' in resp.data[1])
        self.assertTrue('first_name' in resp.data[2])

        # Last names should be visible
        self.assertTrue('last_name' in resp.data[0])
        self.assertTrue('last_name' in resp.data[1])
        self.assertTrue('last_name' in resp.data[2])

    def test_anonymous_serializer_view(self):
        # Request the user list API as an anonymous user
        self.client.logout()
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code, 200)

        # ID, username, first name and last name should always be visible
        self._test_always_visible_fields(resp)

        # Admin users should have their email address included, normal users not.
        self.assertTrue('email' in resp.data[0])
        self.assertTrue('email' not in resp.data[1])
        self.assertTrue('email' not in resp.data[2])

    def test_admin_serializer_view(self):
        # Request the user list API as an admin user
        self.client.login(username='user1', password='user1')
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code, 200)

        # ID, username, first name and last name should always be visible
        self._test_always_visible_fields(resp)

        # Admins should be able to see all e-mail addresses.
        self.assertTrue('email' in resp.data[0])
        self.assertTrue('email' in resp.data[1])
        self.assertTrue('email' in resp.data[2])

    def test_user_serializer_view(self):
        # Request the user list API as a normal user
        self.client.login(username='user2', password='user2')
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(resp.status_code, 200)

        # ID, username, first name and last name should always be visible
        self._test_always_visible_fields(resp)

        # Users should be able to see admin and their own e-mail address.
        self.assertTrue('email' in resp.data[0])
        self.assertTrue('email' in resp.data[1])
        self.assertTrue('email' not in resp.data[2])

    def test_anonymous_serializer_change(self):
        # Cache old user data
        old_user = User.objects.get(pk=2)

        # Try changing every possible field as an anonymous user
        self.client.logout()
        url = reverse('user-detail', kwargs={'pk': 2})
        data = json.dumps({k: 'changed@localhost' for k in UserSerializer.Meta.fields})
        resp = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        # Nothing should have changed
        user = User.objects.get(pk=2)

        self.assertEqual(user.id, old_user.id)
        self.assertEqual(user.username, old_user.username)
        self.assertEqual(user.password, old_user.password)
        self.assertEqual(user.first_name, old_user.first_name)
        self.assertEqual(user.last_name, old_user.last_name)
        self.assertEqual(user.email, old_user.email)

    def test_admin_serializer_change(self):
        # Cache old user data
        old_user = User.objects.get(pk=2)

        # Try changing every possible field as an admin user
        self.client.login(username='user1', password='user1')
        url = reverse('user-detail', kwargs={'pk': 2})
        data = json.dumps({k: 'changed@localhost' for k in UserSerializer.Meta.fields})
        resp = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        # Admins can change first name, last name and email of normal users
        user = User.objects.get(pk=2)

        self.assertEqual(user.id, old_user.id)
        self.assertEqual(user.username, old_user.username)
        self.assertEqual(user.password, old_user.password)
        self.assertEqual(user.first_name, 'changed@localhost')
        self.assertEqual(user.last_name, 'changed@localhost')
        self.assertEqual(user.email, 'changed@localhost')

    def test_user_serializer_change(self):
        # Cache old user data
        old_user = User.objects.get(pk=2)

        # Try changing every possible field as a normal user
        self.client.login(username='user2', password='user2')
        url = reverse('user-detail', kwargs={'pk': 2})
        data = json.dumps({k: 'changed@localhost' for k in UserSerializer.Meta.fields})
        resp = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        # Users can change their first name, last name and email
        user = User.objects.get(pk=2)

        self.assertEqual(user.id, old_user.id)
        self.assertEqual(user.username, old_user.username)
        self.assertEqual(user.password, old_user.password)
        self.assertEqual(user.first_name, 'changed@localhost')
        self.assertEqual(user.last_name, 'changed@localhost')
        self.assertEqual(user.email, 'changed@localhost')

    def test_other_user_serializer_change(self):
        # Cache old user data
        old_user = User.objects.get(pk=2)

        # Try changing every possible field as a normal user
        self.client.login(username='user3', password='user3')
        url = reverse('user-detail', kwargs={'pk': 2})
        data = json.dumps({k: 'changed@localhost' for k in UserSerializer.Meta.fields})
        resp = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        # Users can not change other's first name, last name and email
        user = User.objects.get(pk=2)

        self.assertEqual(user.id, old_user.id)
        self.assertEqual(user.username, old_user.username)
        self.assertEqual(user.password, old_user.password)
        self.assertEqual(user.first_name, old_user.first_name)
        self.assertEqual(user.last_name, old_user.last_name)
        self.assertEqual(user.email, old_user.email)
