Getting started
===============

Get up and running with ``django-logical-perms`` in a matter of just minutes.

Requirements
============

``django-logical-perms`` works with Python 2 and 3. Django 1.8 and up are
supported, including Django 2.0. It can integrate with existing API frameworks
but these aren't required to be installed to use it.

* Python 2.7 and 3.3+
* Django 1.8+, including 2.0

The following are optional requirements. If you would like to use the API
integration layer you will need one the following frameworks or write your
own integration layer:

* Tastypie_
* `Django REST framework`_

.. _Django REST Framework: http://www.django-rest-framework.org
.. _Tastypie: http://tastypieapi.org

Installation
============

You can install directly from the GitHub repository.
::

    pip install git+https://github.com/wearespindle/django-logical-perms.git

Now simply add ``django-logical-perms`` to your project's installed apps and
you're good to go. You can optionally configure a few settings which are
documented on the :ref:`configuration` page, but the defaults should work
just fine.