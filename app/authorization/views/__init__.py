from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from authorization.forms import (RegistrationForm, AuthorizationForm,
                                 RestorePasswordForm, ResetPasswordForm)
from authorization.serializers import CurrentUserSerializer

from .authorization import AuthorizationViewSet
from .registration import RegistrationViewSet
from .current_user import CurrentUserView
from .reset_password import ResetPasswordViewSet
from .restore_password import RestorePasswordViewSet
