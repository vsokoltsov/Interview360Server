from . import (
    serializers, transaction, User, Company, CompanyMember, EmployeeSerializer
)
from rest_framework.authtoken.models import Token
from roles.constants import ROLE_IDENTIFIERS
from common.services.email_service import EmailService
from common.serializers.user_serializer import UserSerializer
from django.db.utils import IntegrityError
from profiles.index import UserIndex

roles = ROLE_IDENTIFIERS.keys()


class EmployeeParamsSerializer(serializers.Serializer):
    """ Serializer params class. """

    email = serializers.EmailField(write_only=True)
    role = serializers.IntegerField(write_only=True)

    def validate_email(self, value):
        """ Employee parameter validation. """

        if self.context['user'].email == value:
            raise serializers.ValidationError(
                "You can't add yourself to the company"
            )
        return value

    def validate_role(self, value):
        """ Employee role validation. """

        if str(value) not in roles:
            raise serializers.ValidationError(
                {'role': "Role {} does not exist".format(value)}
            )
        return value


class EmployeesSerializer(serializers.Serializer):
    """ Employees serializer list. """

    employees = EmployeeParamsSerializer(many=True, write_only=True)
    company_id = serializers.IntegerField(write_only=True)

    def create(self, data):
        """ Create employees. """

        employees = []
        try:
            with transaction.atomic():
                for employee in data['employees']:
                    user = self.find_or_create_user(employee['email'])
                    token, _ = Token.objects.get_or_create(user=user)
                    company = Company.objects.get(id=data['company_id'])
                    self.__create_company_member(user, company, employee)
                    UserIndex.store_index(user)
                    self.__send_email(user, company, token)
                    employees.append(user)
                self.context['company_id'] = data['company_id']
                return employees
        except IntegrityError:
            self.errors['employees'] = 'One of these users already\
                                        belongs to a company'
            return False

    def to_representation(self, instance):
        """Represent serializer data."""

        context_value = {'company_id': self.context['company_id']}
        response = super(EmployeesSerializer, self).to_representation(instance)
        response['employees'] = EmployeeSerializer(
            instance, many=True, context=context_value
        ).data
        return response

    def find_or_create_user(self, email):
        """Find or create user by email."""

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
        return user

    def __send_email(self, user, company, token):
        """Send email based on user's state."""

        if not user.password:
            EmailService.sent_personal_employee_invite(
                user, token, company
            )
        else:
            EmailService.send_company_invite_confirmation(
                user, company
            )

    def __create_company_member(self, user, company, employee):
        """Create new company member based on some conditionas."""

        params = {
            'user_id': user.id,
            'company_id': company.id,
            'role': employee['role']
        }
        if user.password:
            params['active'] = True

        CompanyMember.objects.create(**params)
