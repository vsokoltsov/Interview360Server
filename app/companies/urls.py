from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from .views import CompaniesListViewSet

router = DefaultRouter()
router.register('v1/companies', CompaniesListViewSet, base_name='companies')

urlpatterns = [
        url(r'', include(router.urls) )
]
