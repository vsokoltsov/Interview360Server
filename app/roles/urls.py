from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from .views import RolesViewSet

router = DefaultRouter()
router.register('v1/roles', RolesViewSet, base_name='roles')

urlpatterns = [
    url(r'', include(router.urls) )
]
