from rest_framework_nested import routers

from .views import UserProfileViewSet

router = routers.SimpleRouter()
router.register('', UserProfileViewSet, basename='user')


urlpatterns = router.urls
