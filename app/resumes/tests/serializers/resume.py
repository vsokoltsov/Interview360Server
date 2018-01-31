from . import (
    TransactionTestCase, ResumeSerializer, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, mock, Workplace
)
import ipdb

class ResumeSerializerTest(TransactionTestCase):
    """ Tests for ResumeSerializer class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml',
        'workplaces.yaml'
    ]

    def setUp(self):
        """ Setting up testing dependencies """

        self.resume = Resume.objects.first()
        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.skills = [s.id for s in Skill.objects.filter(id__in=[1, 2])]
        self.workplace = Workplace.objects.last()
        self.serializer = ResumeSerializer(self.resume)
        self.params = {
            'title': 'Python developer',
            'user': self.user.id,
            'skills': self.skills,
            'description': 'Resume',
            'salary': 120000
        }

    def test_contain_id(self):
        """ Testing serializer containing id parameter """

        assert self.serializer.data.get('id'), self.resume.id

    def test_contain_title(self):
        """ Testing serializer containing title parameter """

        assert self.serializer.data.get('title'), self.resume.title

    def test_contain_description(self):
        """ Testing serializer containing description parameter """

        assert self.serializer.data.get('description'), self.resume.description

    def test_contain_salary(self):
        """ Testing serializer containing salary parameter """

        assert self.serializer.data.get('salary'), self.resume.salary

    def test_contain_user(self):
        """ Testing serializer containing user parameter """

        assert self.serializer.data.get('user').get('id'), self.resume.user.id

    def test_contain_workplaces(self):
        """ Testing serializer container workplaces parameter """

        assert(
            [ w.get('id') for w in self.serializer.data.get('workplaces') ],
            [ w.id for w in Workplace.objects.all() ]
        )
