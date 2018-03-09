import abc
import cerberus
from cerberus import Validator
from contextlib import contextmanager
from django.db import transaction
from django_pglocks import advisory_lock

from companies.models import CompanyMember
import ipdb

class BaseValidator(cerberus.Validator):
    """ Custom base validator """

    def _validate_equal(self, equal, field, value):
        """ Validates equation of one field to another """

        match_field, match_value = self._lookup_field(equal)
        if value != match_value:
            self._error(field, 'Does not match the {}'.format(match_field))


class FormException(Exception):
    """ Form exception class """

    def __init__(self, *args, **kwargs):
        """ Initialization class; Setting form exception parameters """

        self.field = kwargs.get('field', None)
        self.errors = kwargs.get('errors', None)

        if not self.field:
            raise NotImplementedError('You must set field key')

        if not self.errors:
            raise NotImplementedError('You must set errors key')

        super(Exception, self).__init__(self)


class BaseForm(abc.ABC):
    """ Base form-object class """

    errors = {}

    @property
    @abc.abstractmethod
    def schema(self):
        pass

    def __init__(self, **kwargs):
        """ Base class init method """

        if not self.schema:
            raise NotImplementedError('Subclasses must define schema property')

        self.validator = BaseValidator(self.schema)
        self.obj = kwargs.get('obj', None)
        self.params = kwargs.get('params', None)
        self.current_user = kwargs.get('current_user', None)
        if self.current_user:
            self.params['current_user'] = self.current_user

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

    def set_error_message(self, key, message):
        """ Set custom error message for particular key """

        self.errors[key] = self.errors.get(key, []) + [message]

    @contextmanager
    def submit(self, message=None):
        """ Save object to the database """

        if not self.is_valid(): return False
