from django.db.utils import IntegrityError

from . import (
    transaction, User, Company, CompanyMember, Token
)

from common.forms import BaseForm
from common.schemas import EMAIL_SCHEMA
from common.services.email_service import EmailService

from companies.validators import company_exist
from profiles.index import UserIndex


class EmployeeForm(BaseForm):
    """
    Form object for employees creation.

    :param company_id: Identifier of the company
    :param employees: List of employees' data
    """

    schema = {
        'company_id': {
            'type': 'integer',
            'empty': False,
            'required': True,
            'validator': company_exist
        },
        'employees': {
            'type': 'list',
            'empty': False,
            'required': True,
            'schema': {
                'type': 'dict',
                'schema': {
                    'email': EMAIL_SCHEMA,
                    'role': {
                        'type': 'integer',
                        'empty': False,
                        'required': True,
                        'allowed': [role[0] for role in CompanyMember.ROLES]
                    }
                }
            }
        }
    }

    def __init__(self, **kwargs):
        """
        Redefine BaseForm constructor. Initial a list of objects
        :param self: EmployeeForm instance
        :param kwargs: Key-value arguments for parent class
        """

        super(EmployeeForm, self).__init__(**kwargs)
        self.data = {
            'employees': [],
            'company_id': kwargs.get('params', {}).get('company_id')
        }

    def submit(self):
        """
        Create new members for the particular company.
        """

        if not self.is_valid():
            return False

        try:
            with transaction.atomic():
                for employee_json in self.params.get('employees', []):
                    user = self.find_or_create_user(employee_json['email'])
                    token, _ = Token.objects.get_or_create(user=user)
                    company = Company.objects.get(id=self.params['company_id'])
                    self.__create_company_member(user, company, employee_json)
                    UserIndex.store_index(user)
                    self.__send_email(user, company, token)
                    self.data['employees'].append(user)
                return True
        except IntegrityError:
            self.errors['employees'] = 'One of these users already\
                                        belongs to a company'
            return False

    def __create_company_member(self, user, company, employee):
        """
        Create new company member.

        :param self: Instance of EmployeeForm's class
        :param user: User, who will be added to company
        :param company: Company, for which the update is performing
        :param employee: JSON data of the new company's employee
        :rtype: CompanyMember
        :return: Newly created CompanyMember's instance
        """

        params = {
            'user_id': user.id,
            'company_id': company.id,
            'role': employee['role']
        }
        if user.password:
            params['active'] = True

        CompanyMember.objects.create(**params)

    def find_or_create_user(self, email):
        """
        Find or create user by email.

        :param self: Instance of EmployeeForm's class
        :param email: User's email
        :rtype: User
        :return: User instance
        """

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
        return user

    def __send_email(self, user, company, token):
        """
        Send email based on user's state.

        :param self: Instance of EmployeeForm's class
        :param user: User for the email notification
        :param company: Company which user is belong
        :param token: User's authorization token based on which
            identification on the email will be performed.
        :rtype: None
        """

        if not user.password:
            EmailService.sent_personal_employee_invite(
                user, token, company
            )
        else:
            EmailService.send_company_invite_confirmation(
                user, company
            )
