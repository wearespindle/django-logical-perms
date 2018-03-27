.. _combining_permissions:

Combining permissions
#####################

Logical permissions make your ordinary permissions smart. You can incorporate any logic in them and they even
integrate with Django's authentication and permissions framework. Besides having logic inside your custom
permissions, you can also combine them logically.

To combine permissions you can simply chain them together using Python's logical operators. There following operators
are currently supported.

Supported operators
-------------------

+----------+---------------------------------------------------------------------+---------------------+
| Operator | Explanation                                                         | Example             |
+==========+=====================================================================+=====================+
| ``&``    | And: Both permissions should evaluate to True.                      | ``perm_a & perm_b`` |
+----------+---------------------------------------------------------------------+---------------------+
| ``|``    | Or: One or both of the permissions should evaluate to True.         | ``perm_a | perm_b`` |
+----------+---------------------------------------------------------------------+---------------------+
| ``^``    | Xor: One, but not both, of the permissions should evaluate to True. | ``perm_a ^ perm_b`` |
+----------+---------------------------------------------------------------------+---------------------+
| ``~``    | Invert: Inverts the result of the permission.                       | ``~perm_a``         |
+----------+---------------------------------------------------------------------+---------------------+

Caching
-------

One of the awesome tricks that combined permissions have up their sleeve is that they can combine individual
permissions. Let's say that we have two logical permissions: ``perm_a`` and ``perm_b``. If we combine these two
multiple times, they will only have to be evaluated once. The individual permissions will cache their output for the
given user and object so that they don't have to be evaluated multiple times.

The following should give a nice impression of this behavior.
::

    @permission
    def perm_a(user, obj=None):
        time.sleep(1)  # sleep 1 second
        return True

    @permission
    def perm_b(user, obj=None):
        time.sleep(1)  # sleep 1 second
        return True

    perm_a(user)  # will take 1 second
    perm_a(user)  # immediate, will use cached result

    perm_b(user)  # will take 1 second
    perm_b(user)  # immediate, will use cached result

    (perm_a & perm_b)(user)  # immediate, uses individual cached results

Examples
--------

Let's have a look at some more examples.
::

    @permission
    def perm_a(user, obj=None):
        return True

    @permission
    def perm_b(user, obj=None):
        return obj is None

``perm_a`` will always evaluate to True while ``perm_b`` will only do so when no object gets passed in.
::

    combined_and = perm_a & perm_b
    combined_or = perm_a | perm_b
    combined_xor = perm_a ^ perm_b

Combining permissions will yield a new permission object which can be saved into a variable. You can even register them.
::

    from django_logical_perms.storages import default_storage

    default_storage.register(combined_and, label='myapp.perm_a_and_b')
    default_storage.register(perm_a | perm_b, label='myapp.perm_a_or_b')

Let's evaluate the permissions.
::

    perm_a(user)  # True
    perm_b(user)  # True

    combined_and(user)  # True
    combined_or(user)  # True
    combined_xor(user)  # False

    user.has_perm('myapp.perm_a_and_b')  # True
    user.has_perm('myapp.perm_a_or_b')  # True

This also works for inverting a permission.
::

    inverted_perm = ~perm_a

    inverted_perm(user)  # False
    (~perm_b)(user)  # False
    (~combined_and)(user)  # True

You can even combine combined permissions.
::

    advanced_perm = (perm_a & perm_b) | ~perm_b
    advanced_perm(user)  # True

Passing in objects is supported as well.
::

    perm_a(user, obj)  # True
    perm_b(user, obj)  # False

    combined_and(user, obj)  # False
    (~perm_b)(user, obj)  # True
    (perm_b ^ perm_a)(user, obj)  # True

Debugging
---------

During development you may run into the problem that you're not sure how the permissions have been combined or that
they yield unexpected results. You can simply request the representation of the permissions to find out how they were
combined. This also works for non-combined permissions.
::

    repr(perm_a)  # P(myapp.perm_a)
    repr(perm_b)  # P(myapp.perm_b)

    repr(~perm_a)  # Not<P(myapp.perm_a)>
    repr(~perm_b)  # Not<P(myapp.perm_b)>

    repr(perm_a & perm_b)  # And<P(myapp.perm_a), P(myapp.perm_b)>
    repr(perm_a | perm_b)  # Or<P(myapp.perm_a), P(myapp.perm_b)>

    repr((perm_a & perm_b) ^ perm_a)  # Xor<And<P(myapp.perm_a), P(myapp.perm_b)>, P(myapp.perm_a)>

    # .. and so on

Where to go from here
---------------------

    **Next up**

        * :ref:`integrating_django`
        * :ref:`integrating_api_frameworks`
        * :ref:`configuration`

    **Advanced topics**

        * :ref:`permissions_module`