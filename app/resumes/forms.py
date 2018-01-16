import cerberus
from cerberus import Validator
import ipdb

class WorkplaceForm:
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
                    'title': {
                        'type': 'string'
                    }
                }
            }
        }
    }
    errors = {}

    def __init__(self, params=None):
        """ Base constructor; Create validator instance and assign parameters """

        self.validator = Validator(self.schema)
        self.params = params

    def submit(self):
        """ Check the from validation and create workplaces """

        if not self.is_valid(): return False

    def is_valid(self):
        """ Return whether or not the receiving data are valid """

        try:
            result = self.validator.validate(self.params, self.schema)
            if not result:
                self.errors = self.validator.errors

            return result
        except cerberus.validator.DocumentError:
            self.errors['workplaces'] =  ['Invalid structure']
            return False
