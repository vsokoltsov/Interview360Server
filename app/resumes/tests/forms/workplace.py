from . import (
    TransactionTestCase, HR, EMPLOYEE, CANDIDATE,
    Company, Resume, mock, WorkplaceForm, Workplace
)
import ipdb

class WorkplaceFormTest(TransactionTestCase):
    """ Tests for the WorkplaceForm class """

    fixtures = [
        'user.yaml',
        'company.yaml',
        'skill.yaml',
        'resume.yaml'
    ]

    def setUp(self):
        """ Setting up testing dependencies """

        self.resume = Resume.objects.last()
        self.company = Company.objects.first()
        self.user = self.company.get_employees_with_role(EMPLOYEE)[0]
        self.params = {
            'workplaces': [
                {
                    'position': 'QA',
                    'resume_id': self.resume.id,
                    'company': self.company.name,
                    'description': 'Bla-bla',
                    'start_date': '2015-02-01',
                    'end_date': '2017-02-01'
                }
            ]
        }

    def test_success_validation(self):
        """ Test success validation of the form """

        form = WorkplaceForm(params=self.params)
        self.assertTrue(form.is_valid())

    def test_failed_validation(self):
        """ Test failed validation without any parameters """

        form = WorkplaceForm(params={})
        self.assertFalse(form.is_valid())

    def test_failed_validation_workplaces_error(self):
        """ Test failed validation workplace error key """

        form = WorkplaceForm(params={})
        form.submit()
        self.assertTrue('workplaces' in form.errors)

    def test_failed_validation_with_empty_workplaces_list(self):
        """ Test failed validation in case of empty workplaces list """

        form = WorkplaceForm(params={ 'workplaces': [] })
        form.submit()
        self.assertTrue('workplaces' in form.errors)

    def test_failed_validation_with_abscent_resume(self):
        """ Test failed validation if resume does not exist """

        self.params['workplaces'][0]['resume_id'] = 10000
        form = WorkplaceForm(params=self.params)
        self.assertFalse(form.is_valid())

    def test_success_creation_of_workplace(self):
        """ Test success creation of the workplace """

        workplaces_count = Workplace.objects.count()
        form = WorkplaceForm(params=self.params)
        form.submit()
        assert Workplace.objects.count(), workplaces_count + 1

    def test_new_workplace_company_value(self):
        """ Test assert of the company to the new workplace """

        form = WorkplaceForm(params=self.params)
        form.submit()
        self.assertTrue(Workplace.objects.last().company_id == self.company.id)


    def test_receiving_of_workplaces_list(self):
        """ Test receiving list of the created workplace """

        form = WorkplaceForm(params=self.params)
        form.submit()

        assert form.objects, [Workplace.objects.last()]

    def test_creation_of_new_company(self):
        """ Test creating of the new company if it does not exist """

        companies_count = Company.objects.count()
        self.params['workplaces'][0]['company'] = 'OOO AAA';
        form = WorkplaceForm(params=self.params)
        form.submit()

        assert Company.objects.count(), companies_count + 1
