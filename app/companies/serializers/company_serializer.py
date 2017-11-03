from . import (
    serializers, User, Company, CompanyMember, transaction, AttachmentField
)
from .companies_serializer import CompaniesSerializer
from .employee_serializer import EmployeeSerializer
from common.serializers.base_vacancy_serializer import BaseVacancySerializer
from common.serializers.base_interview_serializer import BaseInterviewSerializer
from attachments.models import Attachment
from interviews.models import Interview
from django_pglocks import advisory_lock
from roles.constants import COMPANY_OWNER
from profiles.index import UserIndex
import ipdb

class CompanySerializer(CompaniesSerializer):
    """ Serialization of Company object """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    start_date = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    city = serializers.CharField(required=True, max_length=255)
    owner_id = serializers.IntegerField(required=True, write_only=True)
    employees = serializers.SerializerMethodField()
    vacancies = serializers.SerializerMethodField()
    interviews = serializers.SerializerMethodField()

    class Meta:
        model = CompaniesSerializer.Meta.model
        fields = CompaniesSerializer.Meta.fields + [
            'owner_id', 'employees', 'vacancies', 'interviews'
        ]

    def get_employees(self, obj):
        """ Receives the list of employees """

        employees_list = obj.employees.prefetch_related('attachments')[:5]
        return EmployeeSerializer(employees_list,
                                         many=True, read_only=True,
                                         context={'company_id': obj.id}).data
    def get_vacancies(self, obj):
        """ Receive a list of vacancies for company """

        vacancies_list = obj.vacancy_set.all()[:5]
        return BaseVacancySerializer(vacancies_list, many=True, read_only=True).data

    def get_interviews(self, obj):
        """ Receive a list of interviews for company """

        interviews = Interview.for_company(obj.id)
        return BaseInterviewSerializer(interviews, many=True, read_only=True).data

    def get_employees_count(self, obj):
        """ Receive number of employees for company """

        try:
            return obj.employees__count
        except AttributeError:
            return obj.employees.count()

    def get_vacancy_count(self, obj):
        """ Receive number of vacancies for company """

        try:
            return obj.vacancy__count
        except AttributeError:
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
                UserIndex.store_index(User.objects.get(id=owner_id))
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
