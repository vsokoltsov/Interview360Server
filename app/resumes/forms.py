import abc
import cerberus
from cerberus import Validator
from contextlib import contextmanager
from django.db import transaction
from django_pglocks import advisory_lock
import ipdb

class BaseForm(abc.ABC):
    """ Base form-object class """

    @property
    @abc.abstractmethod
    def schema(self):
        pass

    def __init__(self, **kwargs):
        """ Base class init method """

        if not self.schema:
            raise NotImplementedError('Subclasses must define schema property')

        self.validator = Validator(self.schema)
        self.obj = kwargs.get('obj', None)
        self.params = kwargs.get('params', None)


    def is_valid(self):
        """ Return whether or not the receiving data are valid """

        try:
            result = self.validator.validate(self.params, self.schema)
            if not result:
                self.errors = self.validator.errors

            return result
        except cerberus.validator.DocumentError:
            self.errors['base'] =  ['Invalid structure']
            return False

    @contextmanager
    def submit(self, message=None):
        """ Save object to the database """

        if not self.is_valid(): return False

        for key, value in self.params.items():
            setattr(self.obj, key, value)

        with transaction.atomic():
            with advisory_lock(message if message else 'aaa'):
                self.obj.save()
                yield
                return True

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
    errors = {}

    def submit(self):
        """ Check the from validation and create workplaces """

        if not self.is_valid(): return False
