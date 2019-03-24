from . import DEFAULT_UPLOADS_PATH
from storages.backends.s3boto3 import S3Boto3Storage


class AWSStorage(S3Boto3Storage):
    """ Storage backend for the AWS. """

    location = DEFAULT_UPLOADS_PATH
    file_overwrite = False
