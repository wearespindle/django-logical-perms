from tastypie.api import Api

from .views import UserAPI

api = Api(api_name='user')
api.register(UserAPI())

urlpatterns = api.urls
