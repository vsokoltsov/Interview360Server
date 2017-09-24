from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from .views import AttachmentViewSet

router = DefaultRouter()

router.register('v1/attachments', AttachmentViewSet, base_name='attachments')

urlpatterns = [
        url(r'', include(router.urls) )
]
