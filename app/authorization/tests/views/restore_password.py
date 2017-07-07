from . import APITestCase, User

class ResstorePasswordViewTest(APITestCase):
    """ Test of RestorePassword view class """

    def test_success_restore_password(self):
        """ Test success workflow of restoring user password """

        user = User.objects.create(email="example@mail.com")
        user.set_password('12345678')
        user.save()

        response = self.client.post('/api/v1/restore_password/',  {
                'email': 'example@mail.com'
        })

        self.assertEqual('message' in response.data, True)
