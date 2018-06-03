from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from .views import SkillsViewSet

router = DefaultRouter()
router.register('v1/skills', SkillsViewSet, base_name='skills')

urlpatterns = [
    url(r'', include(router.urls))
]
