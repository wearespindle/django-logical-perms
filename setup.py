from setuptools import setup

__title__ = 'django-logical-perms'
__author__ = 'Devhouse Spindle'
__email__ = 'opensource@wearespindle.com'
__version__ = '0.1'
__copyright__ = 'Copyright (C) 2018 Devhouse Spindle'
__license__ = 'MIT License'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = ''

setup(
    name=__title__,
    version=__version__,
    description='Super awesome logical permissions for Django.',
    long_description=long_description,
    author=__author__,
    author_email=__email__,
    license=__license__,
    url='https://github.com/wearespindle/django-logical-perms',
    download_url='https://github.com/wearespindle/django-logical-perms.git',
    packages=[
        'django_logical_perms',
    ],
    install_requires=[
        'Django>=1.8.0',
    ],
    tests_require=[
        'djangorestframework==3.7.7',
        'django-tastypie==0.14.0',
        'nose',
        'coverage',
    ],
    zip_safe=False,
    test_suite='tests.runtests.start',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
