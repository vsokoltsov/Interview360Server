import app
import os
from os.path import abspath, join, dirname
from tempfile import mkdtemp
from shutil import rmtree
from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
import mock


class AttachmentViewSet(APITestCase):
    """Tests class for AttachmentViewSet."""

    def setUp(self):
        """Set up testing dependencies."""

        self.media_folder = mkdtemp()
        if not os.path.exists(app.settings.MEDIA_ROOT):
            os.makedirs(app.settings.MEDIA_ROOT)

        if not os.path.exists(app.settings.THUMBS_ROOT):
            os.makedirs(app.settings.THUMBS_ROOT)

    def tearDown(self):
        """Remove all dependencies after test."""

        dir_path = app.settings.MEDIA_ROOT
        for f in os.listdir(dir_path):
            file_path = "{}/{}".format(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)

    @mock.patch('storages.backends.s3boto3.S3Boto3Storage', FileSystemStorage)
    def test_success_photo_upload(self):
        """Test successfull photo upload."""

        photo_path = join(dirname(app.__file__), 'fixtures/test.jpg')

        with open(photo_path, 'rb') as photo:
            with override_settings(MEDIA_ROOT=self.media_folder):
                resp = self.client.post('/api/v1/attachments/', {
                    'content_type': 'authorization.user',
                    'data': photo
                })
                self.assertEqual(resp.status_code, 200)

    @mock.patch('storages.backends.s3boto3.S3Boto3Storage', FileSystemStorage)
    def test_failed_photo_upload(self):
        """Test failed photo upload."""

        photo_path = join(dirname(app.__file__), 'fixtures/test.jpg')

        with open(photo_path, 'rb'):
            with override_settings(MEDIA_ROOT=self.media_folder):
                resp = self.client.post('/api/v1/attachments/', {})
                self.assertEqual(resp.status_code, 400)
                self.assertTrue('errors' in resp.data)
