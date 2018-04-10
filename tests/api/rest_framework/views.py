from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializers import UserSerializer


class UserAPI(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
