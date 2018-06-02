from . import forms, User, Token, transaction

from django.core.exceptions import ObjectDoesNotExist


class ResetPasswordForm(forms.Form):
    """Reset password form class."""

    token = forms.CharField(required=True)
    password = forms.CharField(max_length=255, min_length=6)
    password_confirmation = forms.CharField(max_length=255, min_length=6)

    def clean(self):
        """Clean data and add custom validation."""

        cleaned_data = super(ResetPasswordForm, self).clean()

        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                self.add_error(
                    'password_confirmation',
                    'Does not match password')
                raise forms.ValidationError("Does not match password")
        return cleaned_data

    def submit(self):
        """Find user by token and change his password."""

        if not self.is_valid():
            return False

        try:
            with transaction.atomic():
                user = User.objects.get(auth_token=self['token'].value())
                user.set_password(self['password'].value())
                user.save()
                return True
        except ObjectDoesNotExist:
            self.add_error('password', 'There is no such user')
            return False
