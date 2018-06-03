from . import forms, User, Token, transaction

import os
from django.core.exceptions import ObjectDoesNotExist
from common.services import EmailService


class RestorePasswordForm(forms.Form):
    """Restore password form class."""

    email = forms.CharField(max_length=255, strip=True)

    def submit(self):
        """Send mail to user with instructions how to reset his password."""

        if not self.is_valid():
            return False

        try:
            with transaction.atomic():
                user = User.objects.get(email=self['email'].value())
                result = Token.objects.get_or_create(user=user)
                auth_token = result[0] if isinstance(result, tuple) else result
                EmailService.send_reset_password_mail(user, auth_token)
                return True
        except ObjectDoesNotExist:
            self.add_error('email', 'There is no such user')
            return False
