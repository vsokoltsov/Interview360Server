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
                        'type': 'string'
                    },
                    'resume_id': {
                        'type': 'integer'
                    },
                    'company': {
                        'type': 'string',
                        'validator': company_exist
                    },
                    'description': {
                        'type': 'string'
                    },
                    'start_date': {
                        'type': 'string',
                        'regex': '^\d{4}-\d{2}-\d{2}$'
                    },
                    'end_date': {
                        'type': 'string',
                        'regex': '^\d{4}-\d{2}-\d{2}$'
                    }
                }
            }
        }
    }

    def company_exist(self, field, value, error):
        """ Custom validation for the company parameter """
        ipdb.set_trace()

    def submit(self):
        """ Check the from validation and create workplaces """

        if not self.is_valid(): return False

        workplaces = self.params.get('workplaces')

        for wp in workplaces:

            workplace = Workplace.objects.create(**wp)
