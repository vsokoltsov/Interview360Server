import os
from .default import DEFAULT

cloudwatch_flag = os.environ.get('CLOUDWATCH')

if cloudwatch_flag:
    from .production import PRODUCTION
    LOGGING = PRODUCTION
else:
    LOGGING = DEFAULT
