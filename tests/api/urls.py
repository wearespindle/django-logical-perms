from django.conf.urls import include, url

urlpatterns = [
    url('drf/', include('tests.api.rest_framework.urls')),
    url('tp/', include('tests.api.tastypie.urls')),
]
