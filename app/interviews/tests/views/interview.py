from . import APITestCase, datetime, Token, Company

class InterviewViewSetTests(APITestCase):
    """ Tests for InterviewViewSet class """

    fixtures = [
        "roles.yaml",
        "skill.yaml",
        "user.yaml",
        "auth_token.yaml",
        "company.yaml",
        "vacancy.yaml",
        "interview.yaml"
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.company = Company.objects.last()
        hr_scope = self.company.get_employees_with_role(2)
        candidate_scope = self.company.get_employees_with_role(4)
        date = datetime.datetime.now() + datetime.timedelta(days=10)
        self.hr = hr_scope.last().user
        self.vacancy = self.company.vacancy_set.first()
        self.candidate = candidate_scope.last().user
        self.interview = self.vacancy.interviews.first()
        self.token = Token.objects.get(user=self.hr)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.form_data = {
            'candidate_id': self.candidate.id,
            'vacancy_id': self.vacancy.id,
            'interviewees': [
                self.hr.id
            ],
            'assigned_at': date
        }
        self.url = "/api/v1/companies/{}/interviews/".format(self.company.id)

    def test_success_list_receiving(self):
        """ Test success receiving list of the interviews """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_success_interview_creation(self):
        """ Test success creation of the interview """

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('interview' in response.data)

    def test_failed_interview_creation(self):
        """ Test failed creation of the interview """

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    def test_success_interview_update(self):
        """ Test success Interview's instance update """

        response = self.client.put(
            self.url + "{}/".format(self.interview.id), self.form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('interview' in response.data)

    def test_success_interview_delete(self):
        """ Test success Interview's instance delete """

        response = self.client.delete(
            self.url + "{}/".format(self.interview.id)
        )
        self.assertEqual(response.status_code, 204)
