from . import (
    APITestCase, mock, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, Token
)
from resumes.index import ResumesIndex
import ipdb

class ResumeViewTest(APITestCase):
    """ Tests for ResumeViewTest """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml'
    ]

    def setUp(self):
        """ Setting up testing dependencies """

        self.resume = Resume.objects.last()
        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.token = Token.objects.create(user=self.user)
        self.skills = [s.id for s in Skill.objects.filter(id__in=[1, 2])]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.params = {
            'title': 'Python developer',
            'user': self.user.id,
            'skills': self.skills,
            'description': 'Resume',
            'salary': 10000
        }

    def test_success_list_receiving(self):
        """ Test success receiving of the list of resumes """

        response = self.client.get('/api/v1/resumes/')
        self.assertEqual(len(response.data), 2)

    def test_success_retrieve_resume(self):
        """ Test success resume retrieving """

        response = self.client.get('/api/v1/resumes/{}/'.format(self.resume.id))
        for key in ['id', 'title', 'description']:
            assert getattr(self.resume, key), response.data[key]

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_success_creation_of_resume(self, resume_index):
        """ Test success creation of the resume """

        response = self.client.post('/api/v1/resumes/', self.params)
        self.assertTrue('resume' in response.data)

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_failed_creation_of_resume(self, resume_index):
        """ Test failed creation of the resume """

        response = self.client.post('/api/v1/resumes/', None)
        self.assertTrue('errors' in response.data)

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_success_update_of_resume(self, resume_index):
        """ Test success update of a resume """

        response = self.client.put(
            '/api/v1/resumes/{}/'.format(self.resume.id), self.params
        )
        self.assertTrue('resume' in response.data)

    @mock.patch.object(ResumesIndex, 'get')
    @mock.patch.object(ResumesIndex, 'delete')
    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_success_deletion_of_resume(self, resume_index, delete_resume, get_resume):
        """ Test success delete of the resume """

        response = self.client.delete(
            '/api/v1/resumes/{}/'.format(self.resume.id)
        )
        assert response.status_code, 204

    @mock.patch('resumes.search.ResumesSearch.find')
    def test_search_action(self, search_mock):
        """ Test success search of resume """

        resume_index = [
            { 'id': 1 },
            { 'id': 2 },
            { 'id': 3 }
        ]
        search_mock.return_value = resume_index
        url = "/api/v1/resumes/search/?q={}".format(
            'buzzword'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['resumes'], resume_index)
