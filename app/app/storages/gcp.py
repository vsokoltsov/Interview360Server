from . import DEFAULT_UPLOADS_PATH
from storages.backends.gcloud import GoogleCloudStorage


class GCPStorage(GoogleCloudStorage):
    """ Custom implemented GCP storage class """

    location = DEFAULT_UPLOADS_PATH
    file_overwrite = False
