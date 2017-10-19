from . import (
    serializers, User, Company, CompanyMember, transaction, AttachmentField
)
from .companies_serializer import CompaniesSerializer
from .employee_serializer import EmployeeSerializer
# from vacancies.serializers import VacancySerializer
from attachments.models import Attachment
from django_pglocks import advisory_lock
from roles.constants import COMPANY_OWNER
import ipdb

BASE_FIELDS = [
    'id',
    'name',
    'city',
    'description',
    'start_date',
    'created_at',
    'owner_id',
    'attachment',
    'employees_count',
    'vacancy_count'
]

class CompanySerializer(CompaniesSerializer):
    """ Serialization of Company object """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    start_date = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    city = serializers.CharField(required=True, max_length=255)
    owner_id = serializers.IntegerField(required=True, write_only=True)
    employees = serializers.SerializerMethodField()

    class Meta:
        model = CompaniesSerializer.Meta.model
        fields = CompaniesSerializer.Meta.fields + [ 'owner_id', 'employees' ]

    def get_employees(self, obj):
        """ Receives the list of employees """

        employees_list = obj.employees.prefetch_related('attachments')[:5]
        return EmployeeSerializer(employees_list,
                                         many=True, read_only=True,
                                         context={'company_id': obj.id}).data
    # def get_vacancies(self, object):
    #     """ Receive a list of vacancies for company """
    #
    #     vacancies_list = obj.vacancy_set.prefetch_related('skills', 'company')[:5]
    #     return VacancySerializer(vacancies_list, many=True, read_only=True).data

    def get_employees_count(self, obj):
        """ Receive number of employees for company """

        return obj.employees.count()

    def get_vacancy_count(self, obj):
        """ Receive number of vacancies for company """

        return obj.vacancy_set.count()

    def validate_owner_id(self, value):
        """ Custom validation for owner_id field """

        try:
            self.owner = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("There is no such user")


    def create(self, validated_data):
        """ Create company method """

        try:
            with transaction.atomic():
                owner_id = validated_data.pop('owner_id', None)
                attachment_json = validated_data.pop('attachment', None)
                company = Company.objects.create(**validated_data)
                company_member = CompanyMember.objects.create(user_id=owner_id,
                                                              company_id=company.id,
                                                              role=COMPANY_OWNER)
                self._create_attachment(attachment_json, company)
                return company
        except:
            return False

    def update(self, instance, validated_data):
        """ Update company method """

        attachment_json = validated_data.pop('attachment', None)
        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.description = validated_data.get('description', instance.description)
        instance.city = validated_data.get('city', instance.city)
        self._create_attachment(attachment_json, instance)
        instance.save()
        return instance

    def _create_attachment(self, attachment_json, instance):

        if attachment_json:
            attachment_id = attachment_json.get('id')
            attachment = Attachment.objects.get(id=attachment_id)
            attachment.object_id=instance.id
            attachment.save()
            return attachment
