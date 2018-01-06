from django.test import TransactionTestCase
from .serializer import ResumeSerializer
from roles.constants import HR, EMPLOYEE, CANDIDATE
from skills.models import Skill
from companies.models import Company
from .models import Resume
import ipdb

class ResumeSerializerTest(TransactionTestCase):
    """ Tests for ResumeSerializer class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml'
    ]

    def setUp(self):
        """ Setting up testing dependencies """

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.skills = [s.id for s in Skill.objects.filter(id__in=[1, 2])]
        self.params = {
            'user': self.user.id,
            'skills': self.skills,
            'description': 'Resume'
        }

    def test_creation_of_resume(self):
        serializer = ResumeSerializer(data=self.params)
        serializer.is_valid()
        serializer.save()
        serializer.data
