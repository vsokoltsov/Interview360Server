from django import forms
from django.db import transaction
from common.advisory_lock import advisory_lock
from rest_framework.authtoken.models import Token

from authorization.models import User

from .registration import RegistrationForm
from .authorization import AuthorizationForm
from .restore_password import RestorePasswordForm
from .reset_password import ResetPasswordForm
