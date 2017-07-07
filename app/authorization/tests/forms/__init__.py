from django.test import TestCase
from authorization.forms import AuthorizationForm, RestorePasswordForm
from authorization.models import User

from .authorization import AuthorizationFormTests
from .restore_password import RestorePasswordFormTests
