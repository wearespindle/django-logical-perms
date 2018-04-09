from tastypie.authorization import DjangoAuthorization


class DjangoObjectAuthorization(DjangoAuthorization):
    """
    Authorization class that will add object-level permission checks to Tastypie's ``DjangoAuthorization`` class.
    """
    def check_user_perm(self, user, permission, obj_or_list):
        if isinstance(obj_or_list, list):
            for obj in obj_or_list:
                if not user.has_perm(permission, obj) and not user.has_perm(permission):
                    return False

            return True

        return user.has_perm(permission, obj_or_list) or user.has_perm(permission)
