from . import (
    TransactionTestCase, HR, EMPLOYEE, CANDIDATE,
    Company, Resume, mock, ResumeForm, Workplace, Skill
)
import ipdb

class ResumeFormTest(TransactionTestCase):
    """ Tests for ResumeForm class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml'
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.resume = Resume.objects.last()
        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.skills = [s.id for s in Skill.objects.filter(id__in=[1, 2])]
        self.params = {
            'title': 'Python developer',
            'user_id': self.user.id,
            'skills': self.skills,
            'description': 'Resume',
            'salary': 120000,
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

    def test_success_validation(self):
        """ Test success validation of form """

        form = ResumeForm(obj=Resume(), params=self.params)
        self.assertTrue(form.is_valid())

    def test_failed_validation_workplaces_error(self):
        """ Test failed validation in case of failed validation of workplaces """

        self.params['workplaces'][0]['position'] = None
        form = ResumeForm(obj=Resume(), params=self.params)
        self.assertFalse(form.submit())

    def test_failed_validation_does_not_create_resume(self):
        """ Test failed validation does not create resume """

        resumes_count = Resume.objects.count()
        self.params['workplaces'][0]['position'] = None
        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert Resume.objects.count(), resumes_count
