from . import serializers, transaction, User, Company, CompanyMember
from rest_framework.authtoken.models import Token
from roles.constants import ROLE_IDENTIFIERS
from rest_framework.authtoken.models import Token
from common.services.email_service import EmailService
from django.db.utils import IntegrityError
from profiles.index import UserIndex
import ipdb

roles = ROLE_IDENTIFIERS.keys()

class EmployeeParamsSerializer(serializers.Serializer):
    """ Serializer params class """

    email = serializers.EmailField()
    role = serializers.IntegerField()

    def validate_email(self, value):
        """ Employee parameter validation """

        if self.context['user'].email == value:
            raise serializers.ValidationError(
                "You can't add yourself to the company"
            )
        return value

    def validate_role(self, value):
        """ Employee role validation """

        if str(value) not in roles:
            raise serializers.ValidationError(
                {'role': "Role {} does not exist".format(value)}
            )
        return value

class EmployeesSerializer(serializers.Serializer):
    """ Employees serializer list """

    employees = EmployeeParamsSerializer(many=True)
    company_id = serializers.IntegerField()

    def create(self, data):
        """ Create employees """

        employees = []
        try:
            with transaction.atomic():
                for employee in data['employees']:
                    user = self.find_or_create_user(employee['email'])
                    token, _ = Token.objects.get_or_create(user=user)
                    company = Company.objects.get(id=data['company_id'])

                    CompanyMember.objects.create(
                        user_id=user.id, company_id=company.id,
                        role=employee['role']
                    )
                    UserIndex.store_index(user)
                    EmailService.sent_personal_employee_invite(
                        user, token, company
                    )
                    employees.append(user)
                return employees
        except IntegrityError as error:
            self.errors['employees'] = 'One of these users already belongs to a company'
            return False

    def find_or_create_user(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
        return user
