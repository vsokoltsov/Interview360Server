from . import (
    APITestCase, mock, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, Token, Workplace
)

class WorkplaceDeleteViewTest(APITestCase):
    """ Test for WorklaceDeleteApiView class """

    fixtures = [
        'user.yaml',
        'skill.yaml',
        'company.yaml',
        'resume.yaml',
        'workplaces.yaml'
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.resume = Resume.objects.last()
        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.workplace = Workplace.objects.last()

    def test_success_workplace_deletion(self):
        """ Test success deletion of the workplace """

        workplaces_count = Workplace.objects.count()
        response = self.client.put(
            '/api/v1/resumes/{}/workplaces/{}/'.format(self.resume.id, self.workplace.id),
            format='json'
        )
        self.assertTrue(response.status_code, 204)
        self.assertTrue(Workplace.objects.count(), workplaces_count - 1)

    def test_failed_workplace_deletion(self):
        """ Test failed deletion of the workplace """

        workplaces_count = Workplace.objects.count()
        response = self.client.put(
            '/api/v1/resumes/{}/workplaces/{}/'.format(self.resume.id, 10000),
            format='json'
        )
        self.assertTrue(response.status_code, 404)
        self.assertTrue(Workplace.objects.count(), workplaces_count)
