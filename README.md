# django-logical-perms

An implementation of logical permissions in Django

## Status

Maintained

## Usage

### Requirements

* Python 2.7
* Python 3.3, 3.4, 3.5
* Django >= 1.8
* Sphinx to build documentation

### Installation

```python
pip install git+https://github.com/wearespindle/django-logical-perms.git
```

### Running

```python
# In your permissions.py.
from django_logical_perms.decorators import permission

@permission(register=True)
def can_contribute(user, repo=None):
    return user.is_staff or repo.public

# In your view.
repo = GitHubRepo('django-logical-perms')

if user.has_perm('app.can_contribute', repo):
    # Do something useful here.
    return render('CONTRIBUERS.md')
```

### Documentation

You can compile the documentation into pretty HTML format:

```bash
cd docs/
make html
open _build/html/index.htm
```

## Contributing

See the [CONTRIBUTING.md](CONTRIBUTING.md) file on how to contribute to this project.

## Contributors

See the [CONTRIBUTORS.md](CONTRIBUTORS.md) file for a list of contributors to the project.

## Roadmap

### Changelog

The changelog can be found in the [CHANGELOG.md](CHANGELOG.md) file.

## Get in touch with a developer

If you want to report an issue see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more info.

We will be happy to answer your other questions at opensource@wearespindle.com

## License

django-logical-perms is made available under the MIT license. See the [LICENSE file](LICENSE) for more info.
