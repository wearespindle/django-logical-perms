.. _autodiscovery:

Permission autodiscovery
========================

If you have added Django logical perms to your ``INSTALLED_APPS`` setting, it will automatically load all permissions
upon starting Django.

How it works
------------

Django fires a signal when apps are done loading. Django logical perms will actually hook into this signal and look
up all loaded apps. For every loaded app, it will try to load the ``permissions.py`` module. You can actually specify
a different module in your settings - have a look at the :ref:`configuration` page for more information.

By loading the permissions modules for all installed apps, the decorators will automatically register the permissions
with the authentication and permissions backend. This way, you can use the permissions with ``user.has_perm()``
without having to import the permissions modules or do other mumbo jumbo.

It's like how Django automatically discovers and loads all your app's models. But for permissions.

Registering permissions
-----------------------

Permissions will automatically register when you pass ``register=True`` into the ``permission`` decorator. In the
following example, the first permission will register automatically. The second will not (unless you explicitly
change your configuration to register all permissions - see :ref:`configuration`).
::

    @permission(register=True)
    def is_staff(user, obj=None):
        return user.is_staff

    @permission
    def is_user(user, obj=None):
        return isinstance(user, User)

Permissions will automatically determine their label based on the app name and method name. You can configure the
format to your own likings or specify a custom label by setting the ``label`` keyword argument.

Some permissions can't automatically be registered because they don't use the ``permission`` decorator. These
permissions can be registered manually. Have a look at the following code snippet.
::

    from django_logical_perms.storages import default_storage
    default_storage.register(is_user)

You can simply put the register calls in your permission modules. They will then register the permissions upon
autodiscovery.

Registering combined permissions
--------------------------------

The same works for combined permissions. If you want to combine permissions and register them under a specific label,
you can simply manually register them to the default storage.
::

    default_storage.register(is_user | is_staff, label='myapp.is_user_or_staff')

Where to go from here
---------------------

You've learned how to integrate Django logical perms with Django's built in authentication and permissions framework.
You'll want to read the following chapters from here on out.

    **Next up**

        * :ref:`integrating_django`
        * :ref:`integrating_api_frameworks`
        * :ref:`configuration`

    **Advanced topics**

        * :ref:`storage`
