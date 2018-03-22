from django_logical_perms.permissions import P


class SimplePermission(P):
    def has_permission(self, user, obj=None):
        return True


class ChangingPermission(P):
    results = {}

    def set_result(self, obj, result):
        self.results[obj] = result

    def has_permission(self, user, obj=None):
        return self.results[obj]
