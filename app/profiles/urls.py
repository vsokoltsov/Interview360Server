from django.conf.urls import url
from django.conf.urls import include

from .views import ProfileViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('v1/users', ProfileViewSet, base_name='users')

urlpatterns = [
    url(r'', include(router.urls))
]
