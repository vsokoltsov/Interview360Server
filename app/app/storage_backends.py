from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """Media storeage, based on S3Boto."""

    location = 'uploads'
    file_overwrite = False
