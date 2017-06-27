from . import forms, transaction, advisory_lock, User, Token
import ipdb

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=255, strip=True)
    password = forms.CharField(max_length=255)

    def submit(self):
        user = User.objects.create(
            email=self['email'].value()
        )
        user.set_password(self['password'].value())

        with transaction.atomic():
            with advisory_lock('User'):
                user.save()
                token = Token.objects.create(user=user)
                return token
