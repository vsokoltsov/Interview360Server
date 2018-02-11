from .base import *
from app.logging.production import LOGGING

DEBUG = False

RAVEN_CONFIG = {
    'dsn': get_environment_variable('SENTRY_KEY')
}
INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]
