from . import forms, User, Token

import ipdb

class AuthorizationForm(forms.Form):
    email = forms.CharField(max_length=255, strip=True)
    password = forms.CharField(max_length=255)

    def submit(self):
        if not self.is_valid(): return False

        try:
            user = User.objects.get(email=self['email'].value())
        except User.DoesNotExist:
            user = None

        if user and user.check_password(self['password'].value()):
            self.token, _ = Token.objects.get_or_create(user=user)
            return True
        else:
            self.add_error('email', 'Invalid credentials')
            return False
