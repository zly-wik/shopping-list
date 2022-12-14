from rest_framework_nested import routers

from .views import UserProfileViewSet, ChecklistViewSet

router = routers.SimpleRouter()
router.register('', UserProfileViewSet, basename='user')
router.register('checklists', ChecklistViewSet, basename='checklist')

urlpatterns = router.urls
