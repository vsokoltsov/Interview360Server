from . import (
    TransactionTestCase, HR, EMPLOYEE, CANDIDATE,
    Company, Resume, mock, ContactForm, Workplace, Skill, Contact
)
import ipdb

class ContactFormTest(TransactionTestCase):
    """ Tests for ContactForm class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml',
        'contacts.yaml'
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.resume = Resume.objects.last()
        self.company = Company.objects.first()
        self.contact = Contact.objects.last()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.params = {
            'resume_id': self.resume.id,
            'email': self.user.email,
            'phone': '+79214438239'
        }

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_validation(self, twilio_mock):
        """ Test success validation of form """

        form = ContactForm(params=self.params)
        self.assertTrue(form.is_valid())

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_validation(self, twilio_mock):
        """ Test failed validation of form """

        form = ContactForm(params={})
        self.assertFalse(form.is_valid())

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_creation_of_contact(self, twilio_mock):
        """ Test success creation of the contact """

        contacts_count = Contact.objects.count()
        form = ContactForm(params=self.params)
        form.submit()
        assert Contact.objects.count(), contacts_count + 1

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_assertion_contact_to_resume(self, twilio_mock):
        """ Test assertion of the contact to the resume """

        form = ContactForm(params=self.params)
        form.submit()
        assert form.obj.resume_id, self.resume.id

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_validation_email_already_exists(self, twilio_mock):
        """ Test failed validation of form if contact with this email
        already exist """

        self.params['email'] = self.contact.email
        form = ContactForm(params=self.params)
        form.submit()
        assert 'email' in form.errors, True

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_validation_phone_already_exists(self, twilio_mock):
        """ Test failed validation of form if contact with this phone
        already exist """

        self.params['phone'] = self.contact.phone
        form = ContactForm(params=self.params)
        form.submit()
        assert 'phone' in form.errors, True
