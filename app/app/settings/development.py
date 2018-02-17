from .base import *
from app.logging.default import LOGGING
import ipdb

DEBUG = True

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]
INSTALLED_APPS += [
    'silk'
]
