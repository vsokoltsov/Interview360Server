import os
import ipdb
import app.environments as environment

app_environment = os.environ.get('DJANGO_DEFAULT_ENV', environment.DEVELOPMENT)

if app_environment == environment.DEVELOPMENT:
    from .development import *
elif app_environment == environment.TEST:
    from .test import *
elif app_environment == environment.PRODUCTION:
    from .production import *
else:
    from .development import *
