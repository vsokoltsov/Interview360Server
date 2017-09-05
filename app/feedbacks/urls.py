from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet

router = DefaultRouter()
router.register('v1/feedbacks', SkillsViewSet, base_name='feedbacks')

urlpatterns = [
    url(r'', include(router.urls) )
]
