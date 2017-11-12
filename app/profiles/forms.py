from django import forms
from django.db import transaction

class ChangePasswordForm(forms.Form):
    """ Change password form for user profile """

    current_password = forms.CharField(max_length=255, min_length=6)
    password = forms.CharField(max_length=255, min_length=6)
    password_confirmation = forms.CharField(max_length=255, min_length=6)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        """ Clean data and add custom validation """

        cleaned_data = super(ChangePasswordForm, self).clean()

        current_password = cleaned_data.get('current_password')
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if not self.user.check_password(current_password):
            current_password_error = 'Does not match current password'
            self.add_error('current_password', current_password_error)
            raise forms.ValidationError(current_password_error)

        print(password)
        if password and password_confirmation:
            if password != password_confirmation:
                password_match_error = 'Does not match password'
                self.add_error('password_confirmation', password_match_error)
                raise forms.ValidationError(password_match_error)
        return cleaned_data

    def submit(self):
        """ Change users password  """

        if not self.is_valid(): return False

        try:
            self.user.set_password(self['password'].value())
            self.user.save()
            return True
        except:
            return False
