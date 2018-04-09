from django_logical_perms.decorators import permission
from django_logical_perms.permissions import LogicalPermission


class SimplePermission(LogicalPermission):
    def has_permission(self, user, obj=None):
        return True


class ChangingPermission(LogicalPermission):
    results = {}

    def set_result(self, obj, result):
        self.results[obj] = result

    def has_permission(self, user, obj=None):
        return self.results[obj]


class StaticLabelPermission(SimplePermission):
    label = 'tests.static_permission'


@permission
def simple_decorated_permission(user, obj=None):
    return True


@permission(label='tests.simple_labeled_permission_custom', register=False)
def simple_labeled_permission(user, obj=None):
    return True


@permission(register=True)
def registered_permission(user, obj=None):
    return True
