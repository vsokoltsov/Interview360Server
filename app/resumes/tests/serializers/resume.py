from . import (
    TransactionTestCase, ResumeSerializer, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, mock
)
import ipdb

class ResumeSerializerTest(TransactionTestCase):
    """ Tests for ResumeSerializer class """

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
        self.skills = [s.id for s in Skill.objects.filter(id__in=[1, 2])]
        self.params = {
            'title': 'Python developer',
            'user': self.user.id,
            'skills': self.skills,
            'description': 'Resume'
        }

    def test_success_validation(self):
        """ Testing success validation of the serializer """

        serializer = ResumeSerializer(data=self.params)
        assert serializer.is_valid(), True

    def test_failed_validation(self):
        """ Testing failed serializer validation """

        serializer = ResumeSerializer(data=None)
        self.assertFalse(serializer.is_valid())

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_success_resume_creation(self, resume_index):
        """ Test success creation of the resume """

        resume_count = Resume.objects.count()
        serializer = ResumeSerializer(data=self.params)
        serializer.is_valid()
        serializer.save()
        assert Resume.objects.count(), resume_count + 1

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_saving_skills_to_resume(self, resume_index):
        """ Save skills to resume """

        serializer = ResumeSerializer(data=self.params)
        serializer.is_valid()
        serializer.save()

        assert(
            [ s.id for s in Resume.objects.last().skills.all() ],
            [ s for s in self.skills ]
        )

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_saving_resume_with_user(self, resume_index):
        """ Test setting user to the new resume """

        serializer = ResumeSerializer(data=self.params)
        serializer.is_valid()
        serializer.save()

        self.assertTrue(Resume.objects.last().user.id, self.user.id)

    @mock.patch('resumes.index.ResumesIndex.store_index')
    def test_success_update_resume(self, resume_index):
        """ Test success resume update """

        serializer = ResumeSerializer(self.resume, data=self.params)
        serializer.is_valid()
        serializer.save()

        self.resume.refresh_from_db()
        assert(
            [ s.id for s in self.resume.skills.all() ],
            [ s for s in self.skills ]
        )
