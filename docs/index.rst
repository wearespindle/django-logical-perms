Logical permissions in Django
=============================

.. image:: https://travis-ci.org/wearespindle/django-logical-perms.svg
    :target: https://travis-ci.org/wearespindle/django-logical-perms
    :alt: Build status
.. image:: https://img.shields.io/github/license/wearespindle/django-logical-perms.svg
   :target: https://github.com/wearespindle/django-logical-perms
   :alt: License

Django_'s default permissions framework is awesome. But for some, it isn't
comprehensive enough. For those, there's ``django-logical-perms``. This module
lets you quickly create complex permissions structures on top of Django's
built-in permissions framework.

We integrate not only with Django itself but also with a few 3rd party Django
modules, such as `Django REST Framework`_ and Tastypie_.

The code is open source and `available on GitHub`_.

.. _Django: https://www.djangoproject.com
.. _Django REST Framework: http://www.django-rest-framework.org
.. _Tastypie: http://tastypieapi.org
.. _available on GitHub: https://github.com/wearespindle/django-logical-perms

.. toctree::
   :maxdepth: 2
   :caption: Documentation
   :glob:

   getting_started
   basic
   autodiscovery
   combining_permissions
   integrating_django
   integrating_api_frameworks
   configuration

.. toctree::
   :maxdepth: 2
   :caption: Advanced topics
   :glob:

   modules/backends
   modules/configs
   modules/decorators
   modules/loaders
   modules/permissions
   modules/storages
   modules/rest_framework
   modules/tastypie
