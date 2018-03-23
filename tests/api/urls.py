from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('drf/', include('tests.api.rest_framework.urls'))
]
