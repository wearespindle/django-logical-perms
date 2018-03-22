from django.conf import settings


def get_permission_label(target):
    label_format = getattr(settings, 'PERMISSION_DEFAULT_LABEL_FORMAT', '{app_name}.{permission_name}')

    return label_format.format(
        app_name='.'.join(target.__module__.split('.')[:-1]),
        permission_name=target.__name__
    )
