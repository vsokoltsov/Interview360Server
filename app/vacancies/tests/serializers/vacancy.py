from . import (
    TransactionTestCase, Vacancy, User, Company, Token, Skill, datetime, mock,
    VacancySerializer, HR
)


class VacancySerializerTest(TransactionTestCase):
    """Test class for VacanciesSerializer."""

    fixtures = [
        'skill.yaml',
        'user.yaml',
        'company.yaml',
        'vacancy.yaml'
    ]

    def setUp(self):
        """Set up testing dependencies."""

        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(HR)[0]
        self.skill = Skill.objects.first()
        self.vacancy = Vacancy.objects.filter(
            company_id=self.company.id).first()

        self.url = "/api/v1/companies/{}/vacancies/".format(self.company.id)
        self.form_data = {
            'title': 'Test',
            'description': 'Test',
            'salary': '150.00',
            'company_id': self.company.id,
            'skills': [
                self.skill.id
            ]
        }

    def test_success_validation(self):
        """Test that validation successfuly passing."""

        serializer = VacancySerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

    def test_failed_validation(self):
        """Test that validation fails."""

        serializer = VacancySerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_failed_skills_are_empty(self):
        """Test validation failure if skills is empty."""

        form_data = {
            'title': 'Test',
            'description': 'Test',
            'salary': '150.00',
            'company_id': self.company.id
        }

        serializer = VacancySerializer(data=form_data)
        self.assertFalse(serializer.is_valid())

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    @mock.patch('vacancies.models.Vacancy.objects.create')
    def test_vacancy_created(self, vacancy_mock, vacancy_index_mock):
        """Test success calling 'create' for Vacancy."""

        vacancy_mock.objects = mock.MagicMock()
        vacancy_mock.objects.create = mock.MagicMock()

        serializer = VacancySerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()

        self.assertTrue(vacancy_mock.called)

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_skills_was_setted(self, vacancy_index_mock):
        """Test success adding of skills to vacancy."""

        serializer = VacancySerializer(data=self.form_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()

        vacancy = Vacancy.objects.last()
        self.assertEqual(len(vacancy.skills.all()), 1)

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_vacancy_was_updated(self, vacancy_index_mock):
        """Test success updating of the vacancy."""

        form_data = {
            'title': 'Test11',
            'description': 'Test',
            'salary': '150.00',
            'company_id': self.company.id,
            'skills': [
                self.skill.id
            ]
        }

        serializer = VacancySerializer(self.vacancy, data=form_data,
                                       partial=True)
        serializer.is_valid()

        v = serializer.save()
        self.assertTrue(v.title == form_data['title'])

    @mock.patch('vacancies.index.VacancyIndex.store_index')
    def test_number_of_skills_was_changed(self, vacancy_index_mock):
        """Test that new skills were applly."""

        new_skill = Skill.objects.create(name="Python")
        form_data = {
            'title': 'Test11',
            'description': 'Test',
            'salary': '150.00',
            'company_id': self.company.id,
            'skills': [
                self.skill.id,
                new_skill.id
            ]
        }

        serializer = VacancySerializer(self.vacancy, data=form_data,
                                       partial=True)

        serializer.is_valid()

        v = serializer.save()
        self.assertEqual(len(v.skills.all()), 2)
