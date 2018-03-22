class P(object):
    """The very base implementation of a logical permission."""

    def __init__(self):
        self.name = self.__class__.__name__

    def has_permission(self, user, obj=None):
        """bool: Tests the permission against a User and an optional object.

        You should override this method to implement custom permission evaluation.

        Note:
            This method should not do caching as that's already handled in the
            ``test`` method below.

        Args:
            user (User): A Django user to test the permission against.
            obj (object, optional): An optional object to do object-level permissions.
        """
        raise NotImplementedError()

    def test(self, user, obj=None):
        """bool: Tests and caches the permission against a User and an optional object.

        Note:
            This method will try getting the result from cache first. If there
            is no cached result available, the permission is evaluated by calling
            ``self.has_permission``. The output will be saved to cache to speed
            up any future lookups.

            You should only override this method if you want to implement your
            own caching algorithm. You should override the ``has_permission``
            method to implement the permission.

        Args:
            user (User): A Django user to test the permission against.
            obj (object, optional): An optional object to do object-level permissions.
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

    def __call__(self, *args, **kwargs):
        """bool: Tests the permissions against a User and an optional object (see test above)."""
        return self.test(*args, **kwargs)

    def __repr__(self):
        """str: Returns textual representation of the permission object."""
        return "P({})".format(self.name)
