"""
Base storages module.
Based on environment variables, set the FileStorage variables
"""

import os
import logging

from app.paths import *
from app.credentials import *
from google.oauth2 import service_account

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
DEFAULT_STORAGE_PROVIDER_MESSAGE = "SELECTED FILE STORAGE PROVIDER - {}"
DEFAULT_UPLOADS_PATH = 'uploads'
DEFAULT_THUMBNAIL_PATH = 'thumbs'
DEFAULT_STATIC_PATH = 'static'
THUMBNAIL_ALIASES = {
    '': {
        'small_thumb': {'size': (50, 50)},
        'thumb': {'size': (100, 100)},
        'medium': {'size': (200, 200)},
        'medium_large': {'size': (250, 250)},
        'large': {'size': (350, 350)}
    },
}
THUMBNAIL_FORCE_OVERWRITE = True
MEDIA_URL = '/{}/'.format(DEFAULT_UPLOADS_PATH)
STATIC_URL = '/{}/'.format(DEFAULT_STATIC_PATH)
THUMBNAIL_BASEDIR = DEFAULT_THUMBNAIL_PATH

if (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and
        AWS_STORAGE_BUCKET_NAME and AWS_REGION_NAME):

    AWS_FILE_STORAGE_CLASS_PATH = 'app.storages.aws.AWSStorage'

    logging.info(DEFAULT_STORAGE_PROVIDER_MESSAGE.format('AWS'))
    DEFAULT_FILE_STORAGE = AWS_FILE_STORAGE_CLASS_PATH
    THUMBNAIL_DEFAULT_STORAGE = AWS_FILE_STORAGE_CLASS_PATH
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    REGION_HOST = 's3.{}.amazonaws.com'.format(AWS_REGION_NAME)
    MEDIA_ROOT = DEFAULT_UPLOADS_PATH
    THUMBS_ROOT = DEFAULT_THUMBNAIL_PATH
elif (GCP_CREDENTIALS_NAME):
    GCP_FILE_STORAGE_CLASS_PATH = 'app.storages.gcp.GCPStorage'
    DEFAULT_FILE_STORAGE = GCP_FILE_STORAGE_CLASS_PATH
    THUMBNAIL_DEFAULT_STORAGE = GCP_FILE_STORAGE_CLASS_PATH
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(
            BASE_DIR, 'app', 'credentials', GCP_CREDENTIALS_NAME
        )
    )
    MEDIA_ROOT = DEFAULT_UPLOADS_PATH
    THUMBS_ROOT = DEFAULT_THUMBNAIL_PATH
else:
    logging.info(DEFAULT_STORAGE_PROVIDER_MESSAGE.format('Local'))

    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
    MEDIA_ROOT = os.path.join(BASE_DIR, DEFAULT_UPLOADS_PATH)
    THUMBS_ROOT = os.path.join(MEDIA_ROOT, DEFAULT_THUMBNAIL_PATH)
