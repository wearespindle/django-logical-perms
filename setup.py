from setuptools import setup

setup(
    name='django-logical-perms',
    version='1.0',
    description='Super awesome logical permissions for Django',
    long_description='Base permissions upon logical methods and integrate them with Django.',
    author='Robert de Vries',
    author_email='meneer@kwieb.com',
    url='https://github.com/wearespindle/django-logical-perms',
    download_url='https://github.com/wearespindle/django-logical-perms.git',
    license='MIT License',
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
    ]
)
