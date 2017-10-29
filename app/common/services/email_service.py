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
        cls._send_default_mail(topic, msg, cls.SENDER, emails)

    @classmethod
    def _send_default_mail(cls, topic, message, sender, mails):
        """ Base mail send function """

        send_mail(topic, message, sender, mails)
