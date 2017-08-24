from django.conf.urls import url
from django.conf.urls import include

from rest_framework_nested import routers

from .views import CompaniesViewSet, EmployeesViewSet, EmployeeActivationView
from vacancies.views import VacancyViewSet

router = routers.SimpleRouter()
router.register('v1/companies', CompaniesViewSet, base_name='companies')

nested_router = routers.NestedSimpleRouter(router, r'v1/companies', lookup='company')
nested_router.register('employees', EmployeesViewSet, base_name="company-employees")
nested_router.register('vacancies', VacancyViewSet, base_name="company-vacancies")

urlpatterns = [
        url(r'', include(router.urls) ),
        url(r'', include(nested_router.urls) ),
        url(r'^v1/companies/(?P<company_id>[A-Za-z0-9]*)/activate_member',
            EmployeeActivationView.as_view()),
]
