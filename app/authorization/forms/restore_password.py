from . import forms, User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string

class RestorePasswordForm(forms.Form):
    """ Send mail to user with instructions how to reset his password """
    email = forms.CharField(max_length=255, strip=True)

    def submit(self):
        if not self.is_valid(): return False

        try:
            user = User.objects.get(email=self['email'].value())
            auth_token, _ = Token.objects.get_or_create(user=user)
            render_to_string('reset_password.html',
                             { 'reset_link_url': 'http://mail.ru',
                              'token': '12345' }
                             )
            return True
        except ObjectDoesNotExist:
            return False
