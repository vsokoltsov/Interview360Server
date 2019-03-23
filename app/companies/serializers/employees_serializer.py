from . import (
    serializers, User, Company, CompanyMember, EmployeeSerializer
)
from common.serializers.user_serializer import UserSerializer


class EmployeesSerializer(serializers.Serializer):
    """ Employees serializer list. """

    employees = UserSerializer(many=True)
    company_id = serializers.IntegerField()
