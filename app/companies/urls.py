from django.conf.urls import url
from django.conf.urls import include

from rest_framework_nested import routers

from .views import CompaniesListViewSet, EmployeesViewSet

router = routers.SimpleRouter()
router.register('v1/companies', CompaniesListViewSet, base_name='companies')

employee_router = routers.NestedSimpleRouter(router, r'v1/companies', lookup='company')
employee_router.register('employees', EmployeesViewSet, base_name="company-employees")

urlpatterns = [
        url(r'', include(router.urls) ),
        url(r'', include(employee_router.urls) )
]
