from django.test import TestCase
import mock
from rest_framework.test import APITestCase
from .models import Skill
from authorization.models import User
from rest_framework.authtoken.models import Token
from .index import SkillIndex
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

        response = self.client.get('/api/v1/skills/', format='json')
        self.assertEqual(len(response.data), 1)

    def test_success_detail_information_receiving(self):
        """ Test success receiving detail infromation """

        response = self.client.get(
            "/api/v1/skills/{}/".format(self.skill.id), format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.data)

    @mock.patch('skills.index.SkillIndex.store_index')
    def test_success_skill_creation(self, skill_index):
        """ Test success creation of the skill """

        response = self.client.post(
            "/api/v1/skills/", self.form_data, format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue('name' in response.data)

    @mock.patch('skills.index.SkillIndex.store_index')
    def test_failed_skill_creation(self, skill_index):
        """ Test failed creation of the skill """

        response = self.client.post(
            "/api/v1/skills/", {}, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('name' in response.data)

    @mock.patch('skills.index.SkillIndex.store_index')
    def test_success_skill_update(self, skill_index):
        """ Test success update of the skill """

        response = self.client.put(
            "/api/v1/skills/{}/".format(self.skill.id),
            self.form_data, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.data)

    @mock.patch('skills.index.SkillIndex.store_index')
    def test_failed_skill_update(self, skill_index):
        """ Test failed update of the skill """

        response = self.client.put(
            "/api/v1/skills/{}/".format(self.skill.id),
            {}, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('name' in response.data)

    @mock.patch.object(SkillIndex, 'get')
    @mock.patch.object(SkillIndex, 'delete')
    @mock.patch('skills.index.SkillIndex.store_index')
    def test_success_skill_deletion(self, skill_index, skill_delete, skill_get):
        """ Test success deletion of the skill """

        response = self.client.delete(
            "/api/v1/skills/{}/".format(self.skill.id), format='json'
        )
        self.assertEqual(response.status_code, 204)

    @mock.patch('skills.search.SkillSearch.find')
    def test_search_action(self, search_mock):
        """ Test success search of skill """

        skill_index = [
            { 'id': 1 },
            { 'id': 2 },
            { 'id': 3 }
        ]
        search_mock.return_value = skill_index
        url = "/api/v1/skills/search/?q={}".format(
            'buzzword'
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['skills'], skill_index)
