from . import (
    TransactionTestCase, HR, EMPLOYEE, CANDIDATE,
    Company, Resume, mock, ResumeForm, Workplace, Skill, Contact
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
                    'company': self.company.name,
                    'description': 'Bla-bla',
                    'start_date': '2015-02-01',
                    'end_date': '2017-02-01'
                }
            ],
            'contact': {
                'resume_id': self.resume.id,
                'email': self.user.email,
                'phone': '+79214438239'
            }
        }

    def test_success_validation(self):
        """ Test success validation of form """

        form = ResumeForm(obj=Resume(), params=self.params)
        self.assertTrue(form.is_valid())

    def test_failed_validation(self):
        """ Test failed validation of form """

        form = ResumeForm(obj=Resume(), params={})
        self.assertFalse(form.is_valid())

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_creation_of_resume(self, twilio_mock):
        """ Test success creation of the resume """

        resumes_count = Resume.objects.count()
        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert Resume.objects.count(), resumes_count + 1

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_setting_of_skils_to_resume(self, twilio_mock):
        """ Test setting skils to the resume after creation """

        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert(
            [s.id for s in form.obj.skills.all()],
            self.skills
        )

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_creating_workplace_for_resume(self, twilio_mock):
        """ Test success creation of workplace for resume """

        workplaces_count = Workplace.objects.count()
        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert Workplace.objects.count(), workplaces_count + 1

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_creating_contact_for_resume(self, twilio_mock):
        """ Test success creation of contact for resume """

        contacts_count = Contact.objects.count()
        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert Contact.objects.count(), contacts_count + 1

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_setting_workplace_for_resume(self, twilio_mock):
        """ Test setting workplace to the resume """

        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert(
            [w.id for w in form.obj.workplaces.all()],
            [Workplace.objects.last().id]
        )

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_validation_workplaces_error(self, twilio_mock):
        """ Test failed validation in case of failed validation of workplaces """

        self.params['workplaces'][0]['position'] = None
        form = ResumeForm(obj=Resume(), params=self.params)
        self.assertFalse(form.submit())

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_validation_does_not_create_resume(self, twilio_mock):
        """ Test failed validation does not create resume """

        resumes_count = Resume.objects.count()
        self.params['workplaces'][0]['position'] = None
        form = ResumeForm(obj=Resume(), params=self.params)
        form.submit()
        assert Resume.objects.count(), resumes_count
