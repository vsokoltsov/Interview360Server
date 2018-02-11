from .base import *
from app.logging.default import LOGGING
import ipdb

DEBUG = True

def show_toolbar(request):
    return True

INTERNAL_IPS = ['192.168.99.100', '127.0.0.1', '0.0.0.0']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += ['debug_toolbar']
DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar
    }
