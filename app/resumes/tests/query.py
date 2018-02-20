from django.test import TestCase
from roles.constants import HR, EMPLOYEE, CANDIDATE
from resumes.forms import WorkplaceForm, ResumeForm, ContactForm
from resumes.query import ResumesQuery
from skills.models import Skill
from companies.models import Company
from resumes.models import Resume, Workplace, Contact
import mock
import ipdb


class ResumesQueryTest(TestCase):
    """ Tests for the ResumesQuery class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml'
    ]

    def setUp(self):
        """ setting up testing dependencies """

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.resume_1 = Resume.objects.get(id=1)
        self.resume_2 = Resume.objects.get(id=2)
        self.resume_3 = Resume.objects.get(id=3)
        self.resume_4 = Resume.objects.get(id=4)
        self.skills = [s.id for s in Skill.objects.filter(id__in=[1, 2])]

    def test_receiving_of_the_resumes_list(self):
        """ Test success receiving of the resumes list without any parameter """

        query = ResumesQuery({})
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_1.id, self.resume_2.id, self.resume_3.id, self.resume_4.id]
        )

    def test_matching_of_salary_value(self):
        """ Test matching of the salary value """

        query = ResumesQuery({
            'salary': {
                'min': 120000,
                'max': 250000
            }
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_2.id, self.resume_3.id, self.resume_4.id]
        )


    def test_matching_of_salary_if_min_is_empty(self):
        """ Test matching of the salary if max key is empty; """\
        """ Return default value """

        query = ResumesQuery({
            'salary': {
                'min': 180000,
            }
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_1.id, self.resume_2.id, self.resume_3.id, self.resume_4.id]
        )

    def test_matching_of_skills(self):
        """ Test matching of the skills values """

        query = ResumesQuery({
            'skills': [1]
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_1.id, self.resume_3.id]
        )

    def test_matching_of_skills_if_empty(self):
        """ Test returning of the default skills value"""\
        """ if skills attribute is empty """

        query = ResumesQuery({
            'skills': []
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_1.id, self.resume_2.id, self.resume_3.id, self.resume_4.id]
        )

    def test_matching_the_order_of_list(self):
        """ Return list of resumes with specific order """

        query = ResumesQuery({
            'order': 'salary'
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_1.id, self.resume_3.id, self.resume_4.id, self.resume_2.id]
        )

    def test_opposite_list_order(self):
        """ Return list of resumes with opposite order """

        query = ResumesQuery({
            'order': '-salary'
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_2.id, self.resume_4.id, self.resume_3.id, self.resume_1.id]
        )

    def test_list_of_resumes_with_wrong_order(self):
        """ Return list of resumes with the wrong order value """

        query = ResumesQuery({
            'order': 'company'
        })
        response = query.list()
        self.assertEqual(
            [ item.id for item in response ],
            [self.resume_1.id, self.resume_2.id, self.resume_3.id, self.resume_4.id]
        )
