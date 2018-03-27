Basic usage
###########

Django's built-in permission framework defines permissions on a per-model basis. You can add a custom permission on a
model and grant your users those permissions by simply adding it to a User instance. This approach is simple and
fast, especially with Django's built-in permission caching.

``django-logical-perms`` gives you the tools for creating complex permissions on top of the built-in Django
permissions framework. You'll be able to define custom permissions and implement your very own logic to determine
whether a user should be authorized or not.

Creating permissions
--------------------

.. note::
    It's recommended that you define your permissions in your app's ``permissions.py``. This file is automatically
    loaded by the module when Django loads. You can change this in your settings. Consult the :ref:`configuration`
    page for more information.

Let's create our first permission using the ``permission`` decorator.
::

    @permission
    def can_update_profile(user, obj=None):
        """Allow users to change their own profile and staff to change all profiles"""
        return user == obj or user.is_staff

Using the new permission is as simple as calling the function.
::

    user_a = User.objects.create_user(username='user_a', is_staff=True)
    user_b = User.objects.create_user(username='user_b', is_staff=False)

    can_update_profile(user_a, user_b)  # True
    can_update_profile(user_b, user_a)  # False
    can_update_profile(user_b, user_b)  # True

Registering permissions
-----------------------

You can pass in additional keyword arguments to the decorator in order to automatically register the permission or to
change its label. Registering a permission means that it gets available to Django's built-in ``user.has_perm()``
check. Let's have look at an example.
::

    @permission(register=True)
    def can_update_profile(user, obj=None):
       return True

    @permission(register=True, label='myapp.another_permission')
    def another_permission(user, obj=None):
       return True

You can now simply call these permissions using ``user.has_perm()``.
::

    # Without passing in an object
    user.has_perm('myapp.can_update_profile')
    user.has_perm('myapp.another_permission')

    # With passing in an object
    user.has_perm('myapp.can_update_profile', obj)
    user.has_perm('myapp.another_permission', obj)

.. note::
    There's more information on how to integrate with Django's authentication and permissions framework on the
    :ref:`integrating_django` page.

More advanced permissions
-------------------------

More complex permissions can be implemented by creating class-based permissions. The ``permission`` decorator
is actually just a convenience decorator that will turn your method into a class-based permission. Class-based
permissions should extend the ``P`` class. Let's create a new class-based permission.
::

    class CanUpdateProfile(P):
        def obj_is_special(self, obj):
            return isinstance(obj, SpecialObject)

        def has_permission(self, user, obj=None):
            return self.obj_is_special(obj) or user.is_staff

Using the permissions is as simple as using the permission we created with a decorator.
::

    can_update_profile = CanUpdateProfile()

    can_update_profile(user_a, user_b)
    can_update_profile(user_b, user_a)

The ``P`` class has two main methods that you can override.

    :has_permission:
        This method should simply return whether or not the user is authorized for the given permission. It should
        not do caching of the permission itself as it's already handled by the ``test`` method.

    :test:
        This method is called to evaluate the permission. It has caching and other convenience features
        built-in so that you don't have to do custom caching in your ``has_permission`` method.

        If you don't want caching of the permission, you should override this method. It's signature is ``test
        (self, user, obj=None)``

You will need to manually register class-based permissions to make them available to ``user.has_perm()``. Registering
a permission is simple.
::

    from django_logical_perms.storages import default_storage

    default_storage.register(CanUpdateProfile())
    default_storage.register(CanUpdateProfile(), label='myapp.can_update_profile')

You can optionally also specify the ``label`` keyword argument. This will register your permission with a custom
label. The default is based on the app name and class name.

Where to go from here
---------------------

You've learned how to create basic permissions, optionally register them with the authentication backend and how to
evaluate the custom permissions you create. You'll want to read the following chapters from here on out.

    **Next up**

        * :ref:`integrating_django`
        * :ref:`integrating_api_frameworks`
        * :ref:`configuration`

    **Advanced topics**

        * :ref:`permission_decorator`
        * :ref:`p_class`