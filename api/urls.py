from rest_framework_nested import routers

from .views import UserProfileViewSet

router = routers.SimpleRouter()
router.register('users', UserProfileViewSet, 'user')


urlpatterns = router.urls
