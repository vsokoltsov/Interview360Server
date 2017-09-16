from . import forms, User, Token

import os
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class RestorePasswordForm(forms.Form):
    """ Send mail to user with instructions how to reset his password """
    email = forms.CharField(max_length=255, strip=True)

    def submit(self):
        if not self.is_valid(): return False

        try:
            user = User.objects.get(email=self['email'].value())
            auth_token, _ = Token.objects.get_or_create(user=user)
            msg = render_to_string('reset_password.html', {
                              'reset_link_url': '{}/auth/reset-password'.format(os.environ['DEFAULT_CLIENT_HOST']),
                              'token': auth_token }
                             )
            send_mail("Reset password mail", msg, "Anymail Sender <from@example.com>", [user.email])
            return True
        except ObjectDoesNotExist:
            self.add_error('email', 'There is no such user')
            return False
