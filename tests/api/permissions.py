from django_logical_perms.configs import FieldPermissionConfig, FieldPermissionConfigSet
from django_logical_perms.decorators import permission


@permission
def can_change_profile(user, obj=None):
    """
    Staff can change everyone's profile, users can only change their own.
    """
    return user.is_staff or obj == user


@permission
def can_view_email(user, obj=None):
    """
    View staff emails or your own.
    """
    return obj.is_staff or obj == user


class UserPermissionConfigSet(FieldPermissionConfigSet):
    """
    This is an example ConfigSet for the User model. ConfigSets can be used on non-models as well.

    * Everyone can view the username and first name and last name of all users;
    * Staff can change all user first names, last names and e-mail addresses;
    * Users can change their own first name, last name and e-mail address;
    * Everyone can view staff e-mail address;
    * Users can view their own e-mail address.

    This ConfigSet is used both the rest_framework and tastypie implementations
    of the API.
    """
    field_config = [
        FieldPermissionConfig(
            fields=['first_name', 'last_name'],
            can_view=True,
            can_change=can_change_profile
        ),
        FieldPermissionConfig(
            fields=['email'],
            can_view=can_change_profile | can_view_email,
            can_change=can_change_profile
        )
    ]

    allow_view = ('id', 'username',)
