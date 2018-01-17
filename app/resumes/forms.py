from common.forms import BaseForm
import ipdb

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
                        'type': 'string'
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

    def submit(self):
        """ Check the from validation and create workplaces """

        if not self.is_valid(): return False
