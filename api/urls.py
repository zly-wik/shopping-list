from django.views.generic import TemplateView
from django.urls import path
from rest_framework_nested import routers

from .views import UserProfileViewSet, ChecklistViewSet, ItemViewSet

router = routers.SimpleRouter()
router.register('', UserProfileViewSet, basename='user')
router.register('checklists', ChecklistViewSet, basename='checklist')

nested_router = routers.NestedSimpleRouter(parent_router=router, parent_prefix='checklists', lookup='checklist')
nested_router.register('items', ItemViewSet, basename='item')

urlpatterns = router.urls + nested_router.urls
