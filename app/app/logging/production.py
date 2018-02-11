import logging
from boto3.session import Session

from app.credentials import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
)

boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_REGION_NAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': logging.ERROR,
        'handlers': ['console'],
    },
    'formatters': {
        'simple': {
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'aws': {
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },

    'handlers': {
        'watchtower': {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
                     'boto3_session': boto3_session,
                     'log_group': 'MyLogGroupName',
                     'stream_name': 'MyStreamName',
            'formatter': 'aws',
        },
        'console': {
            'level': logging.DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['watchtower'],
            'propagate': False,
        },
    },
}
