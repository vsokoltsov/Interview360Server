from . import forms, User, Token

from django.core.exceptions import ObjectDoesNotExist
import ipdb

class ResetPasswordForm(forms.Form):
    token = forms.CharField(required=True)
    password = forms.CharField(max_length=255)
    password_confirmation = forms.CharField(max_length=255)

    def clean(self):
        """ Clean data and add custom validation """
        cleaned_data = super(ResetPasswordForm, self).clean()

        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                raise forms.ValidationError("Password confirmation \
                                            does not match the password")
        return cleaned_data

    def submit(self):
        """ Find user by token and change his password """

        try:
            user = User.objects.get(token=self['token'].value())
            user.set_password(password)
            user.save()
            return True
        except ObjectDoesNotExist:
            self.add_error('email', 'There is no such user')
            return False
