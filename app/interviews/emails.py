from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_interview_reminder(users, vacancy, interview):
    """ Sendm mail with remainding about the next interview """

    params = {
        'vacancy': vacancy,
        'interview': interview
    }
    msg = render_to_string('interview_reminder.html', params)
    send_mail("Reset password mail", msg, "Anymail Sender <from@example.com>", [user.email for user in users])
