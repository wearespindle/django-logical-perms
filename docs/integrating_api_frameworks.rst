.. _integrating_api_frameworks:

API framework integrations
==========================

Django logical perms comes with integration layers for both Django REST framework and Tastypie by default. These
layers provide you with support for field-level permissions. Object-based and action-based permissions can already be
implemented by simply registering permissions with Django's built-in authentication and permissions framework.

Defining field-based permissions
--------------------------------

Permissions should be defined in your permissions module. We'll use these permissions in the field-based permissions
configs later on. These configs can then be used by the API frameworks to determine permissions.

Let's say that we want our users to only be able to change their own first name and last name. They are allowed to
view each other's details.
::

    @permission
    def can_view_profile(user, obj=None):
        return True

    @permission
    def can_change_profile(user, obj=None):
        return user == obj

Defining field-based configs
----------------------------

The permission configuration for a particular field can be defined by using a ``FieldPermissionConfig`` instance.
This class accepts a list of fields that your permissions apply to. You can define a ``view`` and ``change`` permission.

Let's elaborate on our example. We want the first name and last name to be viewable by everyone but only changeable
by the user itself.
::

    field_config = FieldPermissionConfig(
        fields=['first_name', 'last_name'],
        can_view=can_view_profile,
        can_change=can_change_profile)

You can even pass in combined permissions to the ``can_view`` and ``can_change`` arguments.

Putting it all together
-----------------------

We can use a ``FieldPermissionConfigSet`` to actually put everything together. The config set accepts multiple
field-based permission configs and can resolve the permissions for various API frameworks.

Let's define our first config set. It's as simple as passing in multiple field configs and setting a few static field
permissions.
::

    class UserFieldPermissionConfigSet(FieldPermissionConfigSet):
        field_config = [
            FieldPermissionConfig(
                fields=['first_name', 'last_name'],
                can_view=can_view_profile,
                can_change=can_change_profile),
        ]

        # Allow anyone to view user ID and username
        allow_view = ('id', 'username',)

The ``UserFieldPermissionConfigSet`` can now be used by various API frameworks to determine field-based permissions.
The exact implementation differs slightly per API framework.

Django REST framework
---------------------

.. note::
    These instructions are specific to Django REST framework.

Django REST framework makes use of API views and serializers. Django logical perms integrates with the serializers -
those are the processors that turn objects into serialized data after all. The perfect place to adjust the
information goes in and goes out.

By extending ``FieldPermissionsSerializer`` you can add ``field_permissions`` to its meta class. Upon serializing,
the serializer will look up field-based permissions through the config set that was set.

The following serializer would base its field permissions on the ``UserFieldPermissionConfigSet`` we implemented
earlier.

.. note::
    Note that the ``field_permissions`` value is an instance of the config set - it's not a reference to the class
    itself. It will not work if you pass only a reference to the class.

::

    class UserSerializer(serializers.FieldPermissionsSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'first_name', 'last_name',)
            field_permissions = UserFieldPermissionConfigSet()

That's it! Now simply implement your API view as you would normally.
::

    class UserAPI(viewsets.ModelViewSet):
        model = User
        queryset = User.objects.all()
        serializer_class = UserSerializer

Tastypie
--------

.. note::
    These instructions are specific to Tastypie.

Tastypie is a bit easier to implement than Django REST framework in the sense that you don't have to explicitly
define your serializer. You can simply use the ``FieldPermissionsMixin`` with your Tastypie ``Resource``
implementation and specify a custom ``field_permissions`` attribute.

Upon serializing the data (called 'hydrating' and 'dehydrating' in Tastypie), the mixin will simply request the
user's permissions and update the serialized data.

The following resource would base its field permissions on the ``UserFieldPermissionConfigSet`` we implemented
earlier.

.. note::
    Note that the ``field_permissions`` value is an instance of the config set - it's not a reference to the class
    itself. It will not work if you pass only a reference to the class.

::

    class UserAPI(FieldPermissionsMixin, ModelResource):
        class Meta:
            queryset = User.objects.all()
            resource_name = 'user'
            allowed_methods = ['get', 'patch']
            limit = 100
            authentication = SessionAuthentication()
            authorization = DjangoObjectAuthorization()
            field_permissions = UserPermissionConfigSet()

Tastypie doesn't support object-level permission lookups by default. The default ``DjangoAuthorization`` class only
checks for simple permissions without an object passed in.

By using the ``DjangoObjectAuthorization`` class provided by Django logical perms you can force Tastypie to pass
object along when doing permission lookups through Django's ``user.has_perm()``. It has a failover that allows for
checking non-object-level permissions if the object-level permissions was not found.

Where to go from here
---------------------

You've learned how to create field-level permission config sets and use them with REST framework and Tastypie. You'll
want to read the following chapters from here on out.

    **Next up**

        * :ref:`configuration`

    **Advanced topics**

        * :ref:`configs_module`
        * :ref:`rest_framework_module`
        * :ref:`tastypie_module`
