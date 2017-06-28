from . import forms, transaction, advisory_lock, User, Token
from django.db.utils import IntegrityError

import ipdb

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=255, strip=True)
    password = forms.CharField(max_length=255)

    def submit(self):
        if not self.is_valid(): return False

        try:
            user = User.objects.create(email=self['email'].value())
            user.set_password(self['password'].value())

            with transaction.atomic():
                with advisory_lock('User'):
                    user.save()
                    self.token = Token.objects.create(user=user)
                    return True
        except IntegrityError as e:
            self.add_error('email', 'Already present')
            return False
