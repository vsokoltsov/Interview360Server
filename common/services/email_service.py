from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os
import ipdb


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

    @classmethod
    def send_interview_invintation(cls, users, vacancy, interview):
        """ Send email with interview invintation """

        params = {
            'vacancy': vacancy,
            'interview': interview
        }
        msg = render_to_string('interview_invitation.html', params)
        topic = 'Interview invintation'
        cls._send_default_mail(topic, msg, users)

    @classmethod
    def sent_personal_employee_invite(cls, user, token, company):
        """ Send email notificaiton about invintation into the company """

        link_url = '{}/auth/invite'.format(
            os.environ['DEFAULT_CLIENT_HOST']
        )
        msg = render_to_string('company_invite.html', {
            'company': company,
            'link_url': link_url,
            'token': token}
        )
        topic = "Company invite mail"
        cls._send_default_mail(topic, msg, [user])

    @classmethod
    def send_reset_password_mail(cls, user, token):
        """ Send reset password email """

        reset_link = '{}/auth/reset-password'.format(
            os.environ['DEFAULT_CLIENT_HOST'])
        msg = render_to_string('reset_password.html', {
            'reset_link_url': reset_link,
            'token': token}
        )
        topic = 'Reset password'
        cls._send_default_mail(topic, msg, [user])

    @classmethod
    def send_company_invite_confirmation(cls, user, company):
        """ Send email with approvement of invite confirmation """

        company_link = '{}/companies/{}/'.format(
            os.environ['DEFAULT_CLIENT_HOST'], company.id
        )
        msg = render_to_string('company_invite_final.html', {
            'link_url': company_link,
            'user': user,
            'company': company
        })
        topic = 'Invite confirmation'
        cls._send_default_mail(topic, msg, [user])

    @classmethod
    def _send_default_mail(cls, topic, message, mails):
        """ Base mail send function """

        send_mail(topic, message, cls.SENDER, mails)
