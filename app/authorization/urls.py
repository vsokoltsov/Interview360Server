from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from .views import (RegistrationViewSet, AuthorizationViewSet,
                    CurrentUserView, RestorePasswordViewSet )

router = DefaultRouter()
router.register('v1/sign_up', RegistrationViewSet, base_name='sign_up')
router.register('v1/sign_in', AuthorizationViewSet, base_name='sign_in')
router.register('v1/restore_password', RestorePasswordViewSet, base_name='restore_password')

urlpatterns = [
        url(r'^v1/current', CurrentUserView.as_view()),
        url(r'', include(router.urls) )
]
