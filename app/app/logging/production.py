import sys
import logging
from .default import LOGGING
from boto3.session import Session

from app.credentials import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
)

if AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID:

    boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION_NAME)
    aws_format = {
        'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
        'datefmt': "%Y-%m-%d %H:%M:%S"
    }
    watchtower_handler = {
        'level': 'DEBUG',
        'class': 'watchtower.CloudWatchLogHandler',
        'boto3_session': boto3_session,
        'log_group': 'MyLogGroupName',
                     'stream_name': 'MyStreamName',
        'formatter': 'aws',
    }
    LOGGING['formatters']['aws'] = aws_format
    LOGGING['handlers']['watchtower'] = watchtower_handler
    LOGGING['loggers']['django']['handlers'] += ['watchtower']
