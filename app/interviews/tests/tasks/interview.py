from . import (
    TestCase, Interview, Notification, remind_about_interview,
    mock, datetime, mail, override_settings
)
import django.core.mail as mail


class InterviewTaskTest(TestCase):
    """ Tests for interview tasks """

    fixtures = [
        "skill.yaml",
        "user.yaml",
        "company.yaml",
        "vacancy.yaml",
        "interview.yaml",
        "notification.yaml"
    ]

    def setUp(self):
        """ Setting up test dependencies """
        Interview.objects.all().update(
            assigned_at=datetime.datetime.now() + datetime.timedelta(hours=1)
        )
        self.interview = Interview.objects.first()

    @mock.patch('notifications.models.Notification.objects.create')
    def test_notification_objects_creation(self, notification):
        """ Test of creating new notifications for the interview """

        notification.objects = mock.MagicMock()
        notification.objects.create = mock.MagicMock()
        notification.objects.create.return_value = Notification(id=1)

        remind_about_interview()

        self.assertTrue(notification.called)
        self.assertEqual(notification.call_count, 2)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_mail_tested(self):
        """ Test of sending the email after calling the function """

        magic_mock = mock.MagicMock(return_value="1")

        remind_about_interview()

        self.assertEqual(len(mail.outbox), 2)
