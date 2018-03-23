from django_logical_perms.utils import get_permission_label


class BaseP(object):
    """The very base implementation of a logical permission."""

    label = None
    """str: Permission label. Used to register the permission and in its representation."""

    def has_permission(self, user, obj=None):
        """Test the permission against a User and an optional object.

        You should override this method to implement custom permission
        evaluation. This method should not do caching as that's already
        handled in the ``test`` method below.

        :param user: A Django User object to test the permission against.
        :param obj: An optional object to do object-level permissions.
        :returns: bool -- Whether or not the user has permission.
        :raises: NotImplementedError
        """
        raise NotImplementedError()

    def test(self, user, obj=None):
        """Test and caches the permission against a User and an optional object.

        Note:
            This method will try getting the result from cache first. If there
            is no cached result available, the permission is evaluated by
            calling ``self.has_permission``. The output will be saved to cache
            to speed up any future lookups.

            You should only override this method if you want to implement your
            own caching algorithm. You should override the ``has_permission``
            method to implement the permission.

        :param user: A Django user to test the permission against.
        :param obj: An optional object to do object-level permissions.
        :returns: bool -- Whether or not the user has permission.
        """
        # Build a cache if it's not yet set
        if not hasattr(user, '_dlp_cache'):
            setattr(user, '_dlp_cache', {})

        # Try returning results from the cache.
        if (self, obj) in user._dlp_cache:
            return user._dlp_cache[(self, obj)]

        # Permission has not yet been cached. Evaluate through ``has_permission``,
        # save to the cache and return the result.
        result = user._dlp_cache[(self, obj)] = self.has_permission(user, obj)

        return result

    def __call__(self, user, obj=None):
        """Test the permissions against a User and an optional object.

        :returns: bool -- Whether or not the user has permission.
        """
        return self.test(user, obj)

    def __repr__(self):
        """Get textual representation of the permission object.

        :returns: str -- Textual representation of the permission object.
        """
        return 'P(%s)' % self.label

    def __or__(self, other):
        return ProcessedP(
            check_func=lambda user, obj=None: self(user, obj) or other(user, obj),
            desc='Or<{}, {}>'.format(self, other))

    def __and__(self, other):
        return ProcessedP(
            check_func=lambda user, obj=None: self(user, obj) and other(user, obj),
            desc='And<{}, {}>'.format(self, other))

    def __xor__(self, other):
        return ProcessedP(
            check_func=lambda user, obj=None: self(user, obj) ^ other(user, obj),
            desc='Xor<{}, {}>'.format(self, other))

    def __invert__(self):
        return ProcessedP(
            check_func=lambda user, obj=None: not self(user, obj),
            desc='Not<{}>'.format(self))


class P(BaseP):
    """A base class for class-based permissions."""

    def __init__(self):
        # Set up a label if it's not statically assigned
        if self.label is None:
            self.label = get_permission_label(self.__class__)


class FunctionalP(BaseP):
    """A wrapper class for small function-based logical permissions."""

    def __init__(self, check_func, label=None):
        """A new logical permission using the passed in ``check_func``.

        :param check_func: The permission evaluator.
        :param label: Custom label for the permission.
        """
        if self.label is None and label is None:
            label = get_permission_label(check_func)

        self.has_permission = check_func
        self.label = label


class ProcessedP(BaseP):
    """A wrapper class for pre-processed permissions.

    This class is especially useful to omit a label and provide your own
    description of the permission that will show up when calling ``repr()``.

    It's currently only used internally when combining or inverting permissions
    so that resulting P instances will show up as  ``Not<P(...)>``,
    ``Or<P(...), P(...)>`` and so on.

    The instance will not have a (auto generated) label, so that they can't be
    registered with permission storage without explicitly giving a label
    during registration.
    """
    def __init__(self, check_func, desc):
        """Initialise a new instance of ProcessedP.

        :param check_func: The permission evaluator.
        :param desc: A description (not a label) for the permission.
        """
        self.has_permission = check_func
        self._desc = desc

    def __repr__(self):
        return self._desc


class UserHasPermPermission(BaseP):
    """Built-in logical permission for Django's ``user.has_perm`` feature.

    You can use this class to combine your own logical permissions with Django's
    static permissions.

    Note:
         It is very important that you make sure not to evaluate a logical
         permission that will in turn evaluate itself again through
         ``user.has_perm``. This is not only important for this built-in
         permission but also in whatever custom logical permission you
         plan to integrate.

         By calling a logical permission, which will, through whatever path,
         evaluate itself again, you risk creating an infinite loop.

    Example:

        >>> @permission
        ... def user_is_staff(user, obj=None):
        ...     return user.is_staff
        ...
        ... staff_or_awesome = user_is_staff | has_perm('awesome')
        ...
        ... staff_or_awesome(user)
    """
    def __init__(self, perm):
        """Initialise a new instance of UserHasPermPermission.

        :param perm: The permission to pass into ``user.has_perm``
        """
        self.label = 'has_permission: {}'.format(perm)
        self.perm = perm

    def has_permission(self, user, obj=None):
        return user.has_perm(self.perm, obj)


has_perm = UserHasPermPermission
