from .base import *
from app.logging.default import LOGGING as logs

DEBUG = True
SILK_ENABLED = os.environ.get("SILK_ENABLED")

if SILK_ENABLED:
    MIDDLEWARE += [
        'silk.middleware.SilkyMiddleware',
    ]
    INSTALLED_APPS += [
        'silk'
    ]

LOGGIN = logs
