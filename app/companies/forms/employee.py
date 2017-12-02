from . import forms, Company, User, CompanyMember, EmailService
from django.core.exceptions import ObjectDoesNotExist
import ipdb

class EmployeeForm(forms.Form):
    """
    Employee form class;
    Updates user information and creates CompanyMember object
    """

    token = forms.CharField(required=True)
    password = forms.CharField(max_length=255, min_length=6, required=False)
    password_confirmation = forms.CharField(max_length=255, min_length=6, required=False)
    company_pk = forms.IntegerField(required=True)

    def clean_password_confirmation(self):
        """ Check matching of password and password confirmation """

        cleaned_data = self.clean()
        if cleaned_data['password'] != cleaned_data['password_confirmation']:
            raise forms.ValidationError('Password confirmation does not match password')
        return cleaned_data['password']

    def submit(self):
        """ Activate company member """

        if not self.is_valid():
            return False

        try:
            user = User.objects.get(auth_token=self['token'].value())
            if not user.password:
                user.set_password(self['password'].value())
                user.save()
            company_member = CompanyMember.objects.get(
                user_id=user.id, company_id=self['company_pk'].value()
            )
            if not company_member.active:
                company = Company.objects.get(id=self['company_pk'].value())
                company_member.active = True
                company_member.save()
                EmailService.send_company_invite_confirmation(user, company)
                return True
            else:
                raise forms.ValidationError('User member is already activated')
        except User.DoesNotExist as error:
            self.add_error('token', 'There is no such user')
            return False
        except CompanyMember.DoesNotExist as error:
            self.add_error('company_pk', 'User does not belong to the company')
            return False
        except forms.ValidationError as error:
            self.add_error('company_pk', 'User member is already activated')
            return False
