from . import forms, User

class AuthorizationForm(forms.Form):
    email = forms.CharField(max_length=255, strip=True)
    password = forms.CharField(max_length=255)

    def submit(self):
        try:
            user = User.objets.get(email=self['email'].value())
        except DoesNotExist:
            user = None

        if user and user.check_password(self['password'].value()):
            token = Token.objects.get_or_create(user=user)
            return token
