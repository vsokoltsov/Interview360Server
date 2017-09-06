from . import (
    TransactionTestCase, mock, FeedbackSerializer,
    Feedback, Interview, HR, EMPLOYEE, CANDIDATE, Company
)

class FeedbackSerializerTest(TransactionTestCase):
    """ Test class for FeedbackSerializer """

    fixtures = [
        "skill.yaml",
        "user.yaml",
        "auth_token.yaml",
        "company.yaml",
        "vacancy.yaml",
        "interview.yaml",
        "feedback.yaml"
    ]

    def setUp(self):
        """ Setting up test depencencies """
        self.company = Company.objects.first()
        self.hr = self.company.get_employees_with_role(HR)[-1]
        self.feedback = Feedback.objects.last()
        self.interview = Interview.objects.first()

        self.form_data = {
            'user': self.hr.id,
            'description': 'AAA',
            'object_id': self.interview.id,
            'content_type': 'interviews.interview'
        }

    def test_success_validation(self):
        """ Test success validation of the serializer """

        serializer = FeedbackSerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """ Test failed validation of the serializer """

        serializer = FeedbackSerializer(data={})
        self.assertFalse(serializer.is_valid())
