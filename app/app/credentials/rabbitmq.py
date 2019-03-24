"""
Module for rabbitmq and celelry credentials.

Based on presence of environment variables, the broker url is configured.
"""

import os

RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')

if RABBITMQ_DEFAULT_USER and RABBITMQ_DEFAULT_PASS:
    broker = 'amqp://{}:{}@rabbit'.format(
        RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS
    )
else:
    broker = 'amqp://localhost'

CELERY_BROKER_URL = broker
