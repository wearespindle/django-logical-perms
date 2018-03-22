from django.conf import settings


class P(object):
    """The very base implementation of a logical permission."""

    label = None
    """str: Permission label. Used to register the permission and in its representation."""

    def __init__(self):
        # Set up a label if it's not statically assigned
        if self.label is None:
            label_format = getattr(settings, 'PERMISSION_DEFAULT_LABEL_FORMAT', '{app_name}.{permission_name}')

            self.label = label_format.format(
                app_name='.'.join(self.__class__.__module__.split('.')[:-1]),
                permission_name=self.__class__.__name__
            )

    def has_permission(self, user, obj=None):
        """Test the permission against a User and an optional object.

        You should override this method to implement custom permission evaluation.
        This method should not do caching as that's already handled in the ``test``
        method below.

        :param user: A Django User object to test the permission against.
        :param obj: An optional object to do object-level permissions.
        :returns: bool -- Whether or not the user has permission (optionally on the specified object).
        :raises: NotImplementedError
        """
        raise NotImplementedError()

    def test(self, user, obj=None):
        """Test and caches the permission against a User and an optional object.

        Note:
            This method will try getting the result from cache first. If there
            is no cached result available, the permission is evaluated by calling
            ``self.has_permission``. The output will be saved to cache to speed
            up any future lookups.

            You should only override this method if you want to implement your
            own caching algorithm. You should override the ``has_permission``
            method to implement the permission.

        :param user: A Django user to test the permission against.
        :param obj: An optional object to do object-level permissions.
        :returns: bool -- Whether or not the user has permission (optionally on the specified object).
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
        """Test the permissions against a User and an optional object (see test above).

        :returns: bool -- Whether or not the user has permission (optionally on the specified object).
        """
        return self.test(user, obj=None)

    def __repr__(self):
        """Get textual representation of the permission object.

        :returns: str -- Textual representation of the permission object.
        """
        return 'P(%s)' % self.label


class FunctionalP(P):
    """A wrapper class for small function-based logical permissions."""

    def __init__(self, check_func):
        """Initialize a new logical permission that will use the passed in ``check_func`` to evaluate the permission.

        :param check_func: The permission evaluator.
        """
        self.has_permission = check_func
        super(FunctionalP, self).__init__()
