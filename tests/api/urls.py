from django.conf.urls import url, include

urlpatterns = [
    url('drf/', include('tests.api.rest_framework.urls')),
    url('tp/', include('tests.api.tastypie.urls')),
]
