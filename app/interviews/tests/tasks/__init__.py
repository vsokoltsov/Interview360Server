from django.test import TestCase
from interviews.models import Interview
from interviews.tasks import remind_about_interview
from notifications.models import Notification
import mock
import datetime
from django.test import override_settings
import django.core.mail as mail

from .interview import InterviewTaskTest
