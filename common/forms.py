import abc
import cerberus
from contextlib import contextmanager


class BaseValidator(cerberus.Validator):
    """Custom base validator."""

    def _validate_equal(self, equal, field, value):
        """Validate equation of one field to another."""

        match_field, match_value = self._lookup_field(equal)
        if value != match_value:
            self._error(field, 'Does not match the {}'.format(match_field))


class FormException(Exception):
    """Form exception class."""

    def __init__(self, *args, **kwargs):
        """Initialize class; Setting form exception parameters."""

        self.field = kwargs.get('field', None)
        self.errors = kwargs.get('errors', None)

        if not self.field:
            raise NotImplementedError('You must set field key')

        if not self.errors:
            raise NotImplementedError('You must set errors key')

        super(Exception, self).__init__(self)


class BaseForm(abc.ABC):
    """Base form-object class."""

    errors = {}

    @property
    @abc.abstractmethod
    def schema(self):
        """Save validation parameters."""
        pass

    def __init__(self, **kwargs):
        """Override base constructor."""

        if not self.schema:
            raise NotImplementedError('Subclasses must define schema property')

        self.validator = BaseValidator(self.schema)
        self.obj = kwargs.get('obj', None)
        self.params = kwargs.get('params', None)
        self.current_user = kwargs.get('current_user', None)
        if self.current_user:
            self.params['current_user'] = self.current_user

    def is_valid(self):
        "" "Return whether or not the receiving data is valid. """

        try:
            result = self.validator.validate(self.params, self.schema)
            if not result:
                self.errors = self.validator.errors

            return result
        except cerberus.validator.DocumentError:
            self.errors['base'] = ['Invalid structure']
            return False

    def set_error_message(self, key, message):
        """Set custom error message for particular key."""

        self.errors[key] = self.errors.get(key, []) + [message]
