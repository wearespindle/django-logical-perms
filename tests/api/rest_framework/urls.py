from rest_framework.routers import DefaultRouter

from tests.api.rest_framework.views import UserAPI

router = DefaultRouter()
router.register(r'user', UserAPI)

urlpatterns = router.urls
