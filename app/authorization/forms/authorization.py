from . import forms, User, Token

class AuthorizationForm(forms.Form):
    email = forms.CharField(max_length=255, strip=True)
    password = forms.CharField(max_length=255)

    def submit(self):
        try:
            user = User.objects.get(email=self['email'].value())
        except User.DoesNotExist:
            user = None

        if user and user.check_password(self['password'].value()):
            token, _ = Token.objects.get_or_create(user=user)
            return token
        else:
            raise ValueError('Invalid credentials')
