.. _integrating_django:

Django integration
==================

Django logical perms is a good Django citizen. It's a standalone app that can easily integrate with Django's
existing permissions framework and even with various Django API frameworks.

This document focuses solely on integrating Django logical perms with Django itself.

Simple integration
------------------

In order to integrate nicely with Django you will have to add ``django_logical_perms`` to your ``INSTALLED_APPS``.
That's pretty much all there is to get started using Django logical perms.

This will enable automatic loading of permissions but does not enable integration with Django's authentication and
permissions frameworks.

Auth & permissions integration
------------------------------

If you want Django logical perms to integrate with Django's built-in authentication and permissions framework you
will need to add the custom authentication backend. It's simple: just add
``django_logical_perms.backends.LogicalPermissionsBackend`` to your ``AUTHENTICATION_BACKENDS`` setting.

The custom authentication backend does not support authenticating users. It will only integrate with ``has_perm``.

Your settings should look like the following.
::

    INSTALLED_APPS = [
        # ...
        'django_logical_perms',
    ]

    AUTHENTICATION_BACKENDS = [
        'django_logical_perms.backends.LogicalPermissionsBackend',
        'django.contrib.auth.backends.ModelBackend'
    ]

Examples
--------

Now that you have integrated Django logical perms with Django's own authentication and permissions frameworks, you
can register your custom logical permissions with Django. Let's define two simple logical permissions which will
always authorize the user.
::

    @permission
    def is_user_cool(user, obj=None):
        return True

    @permission(register=True)
    def is_user_awesome(user, obj=None):
        return True

    @permission(register=True, label='myapp.user_is_a_user')
    def blep(user, obj=None):
        return True

Let's go over these permissions.

    :is_user_cool:
        This permission is by default not getting registered with the authentication and permissions backend. That's
        because ``is_register`` wasn't specified and the default setting is to not register the permission. You can
        change this behaviour in your own settings by having a look at the :ref:`configuration` docs.

    :is_user_awesome:
        This permission is getting registered with the authentication and permissions backend. It's label is not
        explicitly specified so it will be based on the method name. In this case, the label will be
        ``myapp.is_user_awesome``.

    :blep:
        This permission is getting registered with the authentication and permissions backend. It's label is
        explicitly specified. The permission will therefor be registered as ``myapp.user_is_a_user``.

The permissions can be evaluated through the ``user.has_perm`` method now. Let's have a look at how that works.
::

    user.has_perm('myapp.is_user_cool')  # False, permission was not registered
    user.has_perm('myapp.is_user_awesome')  # True, permission was registered
    user.has_perm('myapp.user_is_a_user')  # True, permission was registered
    user.has_perm('myapp.blep')  # False, the label was explicitly changed

You can also pass in objects. Object-level permissions are not supported by the default Django authentication and
permissions framework, but Django logical perms nicely fills up that gap.
::

    user.has_perm('myapp.is_user_awesome', obj)  # True, obj will get passed in

Using the decorator isn't always convenient to register a permission. You can manually register a permission by
calling the ``register`` method on the default storage backend. Let's have a look at an example.
::

    from django_logical_perms.storages import default_storage

    default_storage.register(is_user_cool | is_user_awesome, label='myapp.user_awesome_or_cool')

This also works fine with class-based permissions.

.. important::
    You must register an instance of the class-based permission. Passing in a reference to the class will not work.

::

    class CustomPermission(P):
        def has_permission(user, obj=None):
            return True

    default_storage.register(CustomPermission(), label='myapp.custom_permission')

Both manually registered permissions can now simply be tested against.
::

    user.has_perm('myapp.user_awesome_or_cool')  # True
    user.has_perm('myapp.custom_permission')  # True

.. note::
    More information on manually registering permissions can be found :ref:`here <autodiscovery>`.

Where to go from here
---------------------

You've learned how to integrate Django logical perms with Django's built in authentication and permissions framework.
You'll want to read the following chapters from here on out.

    **Next up**

        * :ref:`integrating_api_frameworks`
        * :ref:`configuration`

    **Advanced topics**

        * :ref:`permission_decorator`
        * :ref:`p_class`