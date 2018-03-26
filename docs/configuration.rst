.. _configuration:

Configuration
=============

The following settings can be configured in your project's ``settings.py`` file.

``PERMISSIONS_DEFAULT_REGISTER_WITH_BACKEND``
---------------------------------------------

    **Default:** ``False``

    Boolean indicating whether to register all permissions that have been created by the ``@permission`` decorator with
    the default storage by default. This will enable you to simply create a decorated function and have it be integrated
    with Django's ``user.has_perm()`` automagically.

    If you disable this setting you can still explicitly specify permissions to be registered through the ``register``
    decorator argument.

``PERMISSIONS_DEFAULT_LABEL_FORMAT``
------------------------------------

    **Default:** ``{app_name}.{perm_name}``

    A string specifying the default permission label format. This is used to determine logical permission labels if they
    haven't been explicitly specified.

        :app_name: A string representing the name of the app that the permission is defined in.
        :perm_name: The name of the logical permission - such as the class name or the function name.

``PERMISSIONS_MODULE_NAME``
---------------------------

    **Default:** ``permissions``

    This setting defines the default permission module name. This is used to autodiscover permissions in your apps. Upon
    start up, the module will look up all installed apps and will try to load all the permission modules.

    If you change this setting you will need to make sure to rename your permission modules as well. Permissions from
    ``permissions.py`` will not be automatically loaded into the system if the setting gets changed to ``authorization``
    (which would load all the ``authorization.py`` files instead).