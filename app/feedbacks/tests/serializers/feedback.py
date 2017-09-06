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

    @mock.patch('feedbacks.models.Feedback.objects.create')
    def test_success_feedback_creation(self, feedback_class_mock):
        """ Test success feedback creation """

        feedback_class_mock.objects = mock.MagicMock()
        feedback_class_mock.objects.create = mock.MagicMock()
        feedback_class_mock.objects.create.return_value = Feedback(id=1)

        serializer = FeedbackSerializer(data=self.form_data)
        serializer.is_valid()
        serializer.save()

        self.assertTrue(feedback_class_mock.called)

    def test_success_feedback_update(self):
        """ Test success feedback update """

        serializer = FeedbackSerializer(self.feedback, data=self.form_data, partial=True)
        serializer.is_valid()
        feedback = serializer.save()
        self.assertEqual(feedback.description, self.form_data['description'])
