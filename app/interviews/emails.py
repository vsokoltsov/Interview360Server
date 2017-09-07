from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

SENDER = 'Anymail Sender <from@example.com>'

def send_interview_reminder(users, vacancy, interview):
    """ Sendm mail with remainding about the next interview """

    params = {
        'vacancy': vacancy,
        'interview': interview
    }
    msg = render_to_string('interview_reminder.html', params)
    topic = 'Reset password mail'
    emails = [user.email for user in users]
    send_default_mail(topic, msg, SENDER, emails)


def send_default_mail(topic, message, sender, mails):
    """ Base mail send function """

    send_mail(topic, message, sender, mails)
