from django.conf.urls import url
from django.conf.urls import include

from rest_framework_nested import routers
from resumes.views import (
    ResumeViewSet, WorkplacesApiView, WorkplacesDeleteApiView,
    ContactApiView
)

router = routers.SimpleRouter()
router.register('v1/resumes', ResumeViewSet, base_name='resumes')

urlpatterns = [
        url(r'', include(router.urls) ),
        url(r'^v1/resumes/(?P<resume_id>[A-Za-z0-9]*)/workplaces/update/',
            WorkplacesApiView.as_view()
        ),
        url(r'^v1/resumes/(?P<resume_id>[A-Za-z0-9]*)/workplaces/(?P<id>[A-Za-z0-9]*)/',
            WorkplacesDeleteApiView.as_view()
        ),
        url(r'^v1/resumes/(?P<resume_id>[A-Za-z0-9]*)/contact/',
            ContactApiView.as_view()
        )
]
