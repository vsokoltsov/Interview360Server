from common.forms import BaseForm
import cerberus
from resumes.models import Resume, Workplace
from companies.models import Company
import ipdb

def company_exist(field, value, error):
    try:
        company = Company.objects.get(name=value)
    except Company.DoesNotExist:
        error(field, 'Does not exist')


class WorkplaceForm(BaseForm):
    """ Workplace form class """

    schema = {
        'workplaces': {
            'required': True,
            'empty': False,
            'type': 'list',
            'schema': {
                'required': True,
                'empty': False,
                'type': 'dict',
                'schema': {
                    'id': {
                        'type': 'integer',
                        'required': False
                    },
                    'position': {
                        'type': 'string',
                        'empty': False,
                        'required': True
                    },
                    'resume_id': {
                        'type': 'integer',
                        'empty': False,
                        'required': True
                    },
                    'company': {
                        'type': 'string',
                        'empty': False,
                        'required': True
                    },
                    'description': {
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
                    'end_date': {
                        'type': 'string',
                        'regex': '^\d{4}-\d{2}-\d{2}$',
                        'required': True
                    }
                }
            }
        }
    }

    def submit(self):
        """ Check the from validation and create workplaces """

        if not self.is_valid(): return False

        workplaces = self.params.get('workplaces')

        for wp in workplaces:
            company_name = workplace.pop('company')
            # company, created = Compan
            workplace = Workplace.objects.create(**wp)
