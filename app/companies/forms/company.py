from common.forms import BaseForm
from django.db import transaction
from authorization.models import User
from companies.models import CompanyMember
import ipdb

def owner_exist(field, value, error):
    """ Check whether or not owner exist """

    try:
        user = User.objects.get(id=value)
    except User.DoesNotExist:
        error(field, 'Does not exist')

class CompanyForm(BaseForm):
    """ Form object for company model """

    schema = {
        'name': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'start_date': {
            'type': 'string',
            'regex': '^\d{4}-\d{2}-\d{2}$',
            'empty': False,
            'required': True
        },
        'description': {
            'type': 'string',
            'empty': True,
            'required': False
        },
        'city': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'owner_id': {
            'type': 'integer',
            'empty': False,
            'required': True,
            'validator': owner_exist
        },
        'current_user': {
            'empty': False,
            'required': True
        }
    }

    def submit(self):
        """ Set attributes to the company instance and save to the database """

        if not self.is_valid(): return False

        try:
            with transaction.atomic():
                self.__set_attributes()
                self.obj.save()
        except:
            return False

    def is_valid(self):
        """ Override the parent class method """

        result = super(CompanyForm, self).is_valid()

        if (self.obj.id and not self.__is_company_member(self.obj, self.current_user)):
            self.set_error_message('company_member', 'Does not belong to company')
            result = False
            
        return result

    def __set_attributes(self):
        for field, value in self.params.items():
            setattr(self.obj, field, value)

    def __is_company_member(self, company_id, user_id):
        """ Check whether or not the current user is the member of the company """

        try:
            CompanyMember.objects.get(company_id=company_id, user_id=user_id)
            return True
        except CompanyMember.DoesNotExist:
            return False
