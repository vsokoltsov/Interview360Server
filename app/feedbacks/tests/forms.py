from django.test import TransactionTestCase
from django.contrib.contenttypes.models import ContentType
import mock

import ipdb

from authorization.factory import UserFactory
from feedbacks.factory import FeedbackFactory
from companies.factory import CompanyFactory, CompanyMemberFactory

from feedbacks.models import Feedback
from feedbacks.forms import FeedbackForm

class FeedbackFormTests(TransactionTestCase):
    """ Test case for Feedback form test """

    def setUp(self):
        """ Setting up testing dependencies """

        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.company = CompanyFactory()

        self.company_member_1 = CompanyMemberFactory(
            user_id=self.user_1.id, company_id=self.company.id
        )
        self.company_member_2 = CompanyMemberFactory(
            user_id=self.user_2.id, company_id=self.company.id
        )
        # self.feedback = FeedbackFactory(
        #     user_id=self.user_1.id, object_id=self.user_2.id,
        #     content_type=ContentType.objects.get_for_model('authorization.User')
        # )
        self.params = {
            'user_id': self.user_1.id,
            'object_id': self.user_2.id,
            'company_id': self.company.id,
            'content_type': 'authorization.user',
            'description': 'TEXT'
        }

    def test_success_validation(self):
        """ Test success validation of the form """

        form = FeedbackForm(params=self.params)
        self.assertTrue(form.is_valid())

    def test_failed_validation(self):
        """ Test failed validation of the form """

        form = FeedbackForm(params={})
        self.assertFalse(form.is_valid())

    def test_success_submit_of_new_feedback(self):
        """ Test success creation of the new feedback """

        feedbacks_count = Feedback.objects.count()
        form = FeedbackForm(params=self.params)
        form.submit()
        self.assertEqual(Feedback.objects.count(), feedbacks_count + 1)
