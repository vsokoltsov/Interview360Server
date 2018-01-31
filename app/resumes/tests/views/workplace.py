from . import (
    APITestCase, mock, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, Token, Workplace
)

class WorkplaceViewTest(APITestCase):
    """ Test for WorklaceViewSet class """

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
        self.params = {
            'workplaces': [
                {
                    'position': 'QA',
                    'resume_id': self.resume.id,
                    'company': self.company.name,
                    'description': 'Bla-bla',
                    'start_date': '2015-02-01',
                    'end_date': '2017-02-01'
                }
            ]
        }

    def test_success_create_request(self):
        """ Test success create of the workplace """

        response = self.client.put(
            '/api/v1/resumes/{}/workplaces/update/'.format(self.resume.id),
            self.params, format='json'
        )
        self.assertTrue(response.status_code, 200)

    def test_failed_create_request(self):
        """ Test failed create request for the workplace """

        response = self.client.put(
            '/api/v1/resumes/{}/workplaces/update/'.format(self.resume.id),
            { 'workplaces': [] }, format='json'
        )
        self.assertTrue(response.status_code, 400)

    def test_success_update_request(self):
        """ Test sucess request for updatin existing workplace """

        self.params['workplaces'][0]['id'] = self.workplace.id

        response = self.client.put(
            '/api/v1/resumes/{}/workplaces/update/'.format(self.resume.id),
            self.params, format='json'
        )
        self.assertTrue(response.status_code, 200)

    def test_failed_update_request(self):
        """ Test failed update request for the workplace """

        self.params['workplaces'][0]['id'] = self.workplace.id

        response = self.client.put(
            '/api/v1/resumes/{}/workplaces/update/'.format(self.resume.id),
            { 'workplaces': [] }, format='json'
        )
        self.assertTrue(response.status_code, 400)
