from common.forms import BaseForm
from django.db import transaction
from authorization.models import User

def owner_exist(field, value, error):
    """ Check whether or not owner exist """

    try:
        user = User.objects.get(id=value)
    except User.DoesNotExist:
        error(field, 'Does not exist')

class CompanyForm(BaseForm):
    """ Form object for company model """

    schema = {
        'id': {
            'type': 'integer',
            'required': False
        },
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
            'required': True,
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


    def __set_attributes(self):
        for field, value in self.params.items():
            setattr(self.obj, field, value)
