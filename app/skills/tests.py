from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Skill
from authorization.models import User
from rest_framework.authtoken.models import Token
import ipdb

class SkillViewSetTests(APITestCase):
    """ View tests for SkillViewTest class """

    def setUp(self):
        """ Setting up the test dependencies """

        self.user = User.objects.create(email="example1@mail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.skill = Skill.objects.create(name="Skill name")
        self.form_data = {
            'name': 'Test skill'
        }

    def test_success_list_receiving(self):
        """ Test success receiving list of skills """

        response = self.client.get('/api/v1/skills/')
        self.assertEqual(len(response.data), 1)

    def test_success_detail_information_receiving(self):
        """ Test success receiving detail infromation """

        response = self.client.get("/api/v1/skills/{}/".format(self.skill.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.data)

    def test_success_skill_creation(self):
        """ Test success creation of the skill """

        response = self.client.post("/api/v1/skills/", self.form_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('name' in response.data)

    def test_failed_skill_creation(self):
        """ Test failed creation of the skill """

        response = self.client.post("/api/v1/skills/", {})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('name' in response.data)

    def test_success_skill_update(self):
        """ Test success update of the skill """

        response = self.client.put(
            "/api/v1/skills/{}/".format(self.skill.id),
            self.form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.data)

    def test_failed_skill_update(self):
        """ Test failed update of the skill """

        response = self.client.put(
            "/api/v1/skills/{}/".format(self.skill.id),
            {}
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('name' in response.data)

    def test_success_skill_deletion(self):
        """ Test success deletion of the skill """

        response = self.client.delete("/api/v1/skills/{}/".format(self.skill.id))
        self.assertEqual(response.status_code, 204)
