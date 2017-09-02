from django.conf.urls import url
from django.conf.urls import include

from rest_framework_nested import routers

from .views import CompaniesViewSet, EmployeesViewSet, EmployeeActivationView
from vacancies.views import VacancyViewSet
from interviews.views import InterviewViewSet, InterviewEmployeeView

router = routers.SimpleRouter()
router.register('v1/companies', CompaniesViewSet, base_name='companies')

nested_router = routers.NestedSimpleRouter(router, r'v1/companies', lookup='company')
nested_router.register('employees', EmployeesViewSet, base_name="company-employees")

vacancies_router = routers.NestedSimpleRouter(router, r'v1/companies', lookup='company')
vacancies_router.register('vacancies', VacancyViewSet, base_name="company-vacancies")

# TODO
# make this router inherited from the company router, not the vacancies_one

interviews_router = routers.NestedSimpleRouter(vacancies_router, r'vacancies', lookup='vacancy')
interviews_router.register('interviews', InterviewViewSet, base_name="vacancy-interviews")

urlpatterns = [
        url(r'', include(router.urls) ),
        url(r'', include(nested_router.urls) ),
        url(r'', include(vacancies_router.urls) ),
        url(r'', include(interviews_router.urls) ),
        url(r'^v1/companies/(?P<company_id>[A-Za-z0-9]*)/activate_member',
            EmployeeActivationView.as_view()),
        url(r'^v1/interviews/(?P<interview_id>[A-Za-z0-9]*)/employees/(?P<employee_id>[A-Za-z0-9]*)',
            InterviewEmployeeView.as_view()),
]
