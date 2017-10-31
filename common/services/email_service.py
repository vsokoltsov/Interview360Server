from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class EmailService:
    SENDER = 'Anymail Sender <from@example.com>'

    @classmethod
    def send_interview_reminder(cls, user, vacancy, interview):
        """ Send mail with remainding about upcoming interview """

        params = {
            'vacancy': vacancy,
            'interview': interview
        }

        msg = render_to_string('interview_reminder.html', params)
        topic = 'Upcoming interview notification'
        emails = [user]
        cls._send_default_mail(topic, msg, emails)

    def send_interview_invintation(cls, users, vacancy, interview):
        """ Send email with interview invintation """

        params = {
            'vacancy': vacancy,
            'interview': interview
        }
        msg = render_to_string('interview_invintation.html', params)
        topic = 'Interview invintation'
        cls._send_default_mail(topic, msg, users)

    @classmethod
    def _send_default_mail(cls, topic, message,mails):
        """ Base mail send function """

        send_mail(topic, message, cls.SENDER, mails)
