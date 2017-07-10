from django.test import TestCase
from authorization.forms import (AuthorizationForm, RestorePasswordForm,
                                 RegistrationForm)
from authorization.models import User

from .authorization import AuthorizationFormTests
from .restore_password import RestorePasswordFormTests
