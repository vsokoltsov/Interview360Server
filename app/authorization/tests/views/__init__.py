from rest_framework.test import APITestCase
from authorization.models import User

from .authorization import AuthorizationViewSetTests
from .registration import RegistrationViewTests
from .current_user import CurrentUserViewTests
from .restore_password import ResstorePasswordViewTest
