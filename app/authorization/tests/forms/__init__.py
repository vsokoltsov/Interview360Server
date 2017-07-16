from django.test import TestCase, TransactionTestCase
from authorization.forms import (AuthorizationForm, RestorePasswordForm,
                                 RegistrationForm, ResetPasswordForm)
from authorization.models import User
from django.test import override_settings
from rest_framework.authtoken.models import Token
import mock

from .authorization import AuthorizationFormTests
from .restore_password import RestorePasswordFormTests
from .registration import RegistrationFormTests
from .reset_password import ResetPasswordFormTest
