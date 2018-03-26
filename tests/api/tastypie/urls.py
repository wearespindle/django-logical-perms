from tastypie.api import Api

from tests.api.tastypie.views import UserAPI

api = Api(api_name='user')
api.register(UserAPI())

urlpatterns = api.urls
