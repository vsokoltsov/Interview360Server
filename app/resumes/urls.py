from django.conf.urls import url
from django.conf.urls import include

from rest_framework_nested import routers
from .views import ResumeViewSet, WorkplaceViewSet

router = routers.SimpleRouter()
router.register('v1/resumes', ResumeViewSet, base_name='resumes')

workplace_router = routers.NestedSimpleRouter(router, r'v1/resumes', lookup='resumes')
workplace_router.register('workplaces', WorkplaceViewSet, base_name="resume-workplaces")

urlpatterns = [
        url(r'', include(router.urls) ),
        url(r'', include(workplace_router.urls) )
]
