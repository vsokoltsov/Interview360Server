from django.conf.urls import url
from django.conf.urls import include

from rest_framework_nested import routers
from .views import ResumeViewSet

router = routers.SimpleRouter()
router.register('v1/resumes', ResumeViewSet, base_name='resumes')

urlpatterns = [
        url(r'', include(router.urls) )
]
