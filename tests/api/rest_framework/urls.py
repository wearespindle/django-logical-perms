from rest_framework.routers import DefaultRouter

from .views import UserAPI

router = DefaultRouter()
router.register(r'user', UserAPI)

urlpatterns = router.urls
