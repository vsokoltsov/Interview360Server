from . import (
    TransactionTestCase, ResumeSerializer, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, mock, Workplace
)


class ResumeSerializerTest(TransactionTestCase):
    """Tests for ResumeSerializer class."""

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml',
        'workplaces.yaml'
    ]

    def setUp(self):
        """Set up testing dependencies."""

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
        """Test serializer containing id parameter."""

        self.assertEqual(self.serializer.data.get('id'), self.resume.id)

    def test_contain_title(self):
        """Test serializer containing title parameter."""

        self.assertEqual(self.serializer.data.get('title'), self.resume.title)

    def test_contain_description(self):
        """Test serializer containing description parameter."""

        self.assertEqual(
            self.serializer.data.get('description'), self.resume.description
        )

    def test_contain_salary(self):
        """Test serializer containing salary parameter."""

        self.assertEqual(
            self.serializer.data.get('salary'), self.resume.salary
        )

    def test_contain_user(self):
        """Test serializer containing user parameter."""

        self.assertEqual(
            self.serializer.data.get('user').get('id'), self.resume.user.id
        )

    def test_contain_workplaces(self):
        """Test serializer container workplaces parameter."""

        self.assertEqual(
            [w.get('id') for w in self.serializer.data.get('workplaces')],
            [w.id for w in Workplace.objects.all()]
        )
