from . import forms, Company, User, CompanyMember, Role
from django.core.exceptions import ObjectDoesNotExist

class EmployeeForm(forms.Form):
    """
    Employee form class;
    Updates user information and creates CompanyMember object
    """

    token = forms.CharField(required=True)
    password = forms.CharField(max_length=255, min_length=6)
    password_confirmation = forms.CharField(max_length=255, min_length=6)
    company_id = forms.IntegerField(required=True)

    def clean_password_confirmation(self):
        """ Check matching of password and password confirmation """

        cleaned_data = self.clean()
        if cleaned_data['password'] != cleaned_data['password_confirmation']:
            raise forms.ValidationError('Password confirmation does not match password')
        return cleaned_data['password']

    def submit(self):
        if not self.is_valid():
            return False

        try:
            user = User.objects.get(auth_token=self['token'].value())
            user.set_password(self['password'].value())
            user.save()
            role = Role.objects.first()
            CompanyMember.objects.create(
                company_id=self['company_id'].value(),
                user_id=user.id,
                role_id=role.id
            )
            return True
        except ObjectDoesNotExist:
            self.add_error('token', 'There is no such user')
            return False
