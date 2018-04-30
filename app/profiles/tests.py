import app
import os
from os.path import abspath, join, dirname
from tempfile import mkdtemp
from shutil import rmtree
from django.core.files import File
from rest_framework.test import APITestCase
from authorization.models import User
from rest_framework.authtoken.models import Token
from attachments.models import Image
from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings
from django.core.files.storage import FileSystemStorage
import mock
import ipdb


class ProfileViewSetTest(APITestCase):
    """ Tests for ProfileViewSet class """

    def setUp(self):
        """ Setting up testing dependencies """

        password = 'aaaaaaaa'
        self.user = User.objects.create(
            email="example1@mail.com", password=password)
        self.token = Token.objects.create(user=self.user)
        self.media_folder = mkdtemp()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.form_data = {
            'email': 'awdawdwad@mail.ru',
            'first_name': 'aaaaa',
            'last_name': 'bbbbb'
        }
        self.password_change_form = {
            'current_pasword': password,
            'password': 'aaaaaa999999',
            'password_confirmation': 'aaaaaa999999'
        }

    def tearDown(self):
        """ Removing all dependencies after test """

        dir_path = app.settings.MEDIA_ROOT
        for f in os.listdir(dir_path):
            file_path = "{}/{}".format(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)

    def test_success_receiving_of_profile(self):
        """ Test success receiving current user information """

        response = self.client.get(
            '/api/v1/users/{}/'.format(self.user.id), format='json'
        )
        assert response.status_code, 200

    @mock.patch('profiles.index.UserIndex.store_index')
    def test_success_update_profile(self, user_index):
        """ Test success update of the profile information """

        response = self.client.put(
            '/api/v1/users/{}/'.format(self.user.id),
            self.form_data, format='json'
        )
        user = User.objects.get(id=self.user.id)
        assert user.email, self.form_data['email']

    def test_success_change_password_route(self):
        """ Test success password change """

        response = self.client.put(
            '/api/v1/users/{}/change_password/'.format(self.user.id),
            self.password_change_form, format='json'
        )
        assert 200, response.status_code

    def test_failed_password_change(self):
        """ Test failed password change """

        response = self.client.put(
            '/api/v1/users/{}/change_password/'.format(self.user.id), {},
            format='json'
        )
        assert 400, response.status_code

    @mock.patch('profiles.index.UserIndex.store_index')
    @mock.patch('storages.backends.s3boto3.S3Boto3Storage', FileSystemStorage)
    def test_update_with_attachment_information(self, boto_mock):
        """ Test update user instance with attahcment field """

        content_type = ContentType.objects.get_for_model(User)
        file_path = join(dirname(app.__file__), 'fixtures/test.jpg')

        with open(file_path, 'rb') as photo:
            attachment = Image(content_type=content_type)
            attachment.data.save('test.jpg', File(photo), 'rb')
            self.form_data['attachment'] = {'id': attachment.id}

            response = self.client.put(
                '/api/v1/users/{}/'.format(self.user.id), self.form_data,
                format='json'
            )

            attachment.refresh_from_db()
            assert attachment.object_id, self.user.id
