from . import (
    APITestCase, mock, HR, EMPLOYEE, CANDIDATE,
    Skill, Company, Resume, Token, Workplace, Contact, User
)
import ipdb

class ContactApiViewTest(APITestCase):
    """ Tests for ContactApiView class """

    fixtures = [
        'user.yaml',
        'skill.yaml',
        'company.yaml',
        'resume.yaml',
        'contacts.yaml'
    ]

    def setUp(self):
        """ Setting up test dependencies """

        self.resume = Resume.objects.first()
        self.company = Company.objects.first()
        self.contact = Contact.objects.last()
        self.user = User.objects.first()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.workplace = Workplace.objects.last()
        self.params = {
            'resume_id': self.resume.id,
            'email': self.user.email,
            'phone': '+79214438239'
        }

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_create_request(self, twilio_mock):
        """ Test success create of the contact """

        response = self.client.put(
            '/api/v1/resumes/{}/contact/'.format(self.resume.id),
            self.params
        )
        self.assertTrue(response.status_code, 200)

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_create_request(self, twilio_mock):
        """ Test failed create of the contact """

        response = self.client.put(
            '/api/v1/resumes/{}/contact/'.format(self.resume.id),
            {}
        )
        self.assertTrue(response.status_code, 400)

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_success_update_request(self, twilio_mock):
        """ Test success update of the contact """

        self.params['id'] = self.contact.id
        response = self.client.put(
            '/api/v1/resumes/{}/contact/'.format(self.resume.id),
            self.params
        )
        self.assertTrue(response.status_code, 200)

    @mock.patch('common.services.twilio_service.TwilioService')
    def test_failed_update_request(self, twilio_mock):
        """ Test failed update of the contact """

        self.params['id'] = self.contact.id
        self.params['phone'] = self.contact.phone
        response = self.client.put(
            '/api/v1/resumes/{}/contact/'.format(self.resume.id),
            self.params
        )
        self.assertTrue(response.status_code, 400)

    def test_success_contact_delete_request(self):
        """ Test success contact delete request """

        contacts_count = Contact.objects.count()
        response = self.client.delete(
            '/api/v1/resumes/{}/contact/'.format(self.resume.id)
        )
        self.assertEqual(Contact.objects.count(), contacts_count - 1)

    def test_failed_deleted_contact_request(self):
        """ Test failed contact delete request """

        contacts_count = Contact.objects.count()
        response = self.client.delete(
            '/api/v1/resumes/{}/contact/'.format(1000)
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Contact.objects.count(), contacts_count)
