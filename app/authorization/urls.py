from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from .views import RegistrationViewSet, AuthorizationViewSet, CurrentUserView

router = DefaultRouter()
router.register('v1/sign_up', RegistrationViewSet, base_name='sign_up')
router.register('v1/sign_in', AuthorizationViewSet, base_name='sign_in')

urlpatterns = [
        url(r'^v1/current', CurrentUserView.as_view()),
        url(r'', include(router.urls) )
]
