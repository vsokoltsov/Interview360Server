from . import (
    serializers, User, Company, CompanyMember, transaction, AttachmentField
)
from .employee_serializer import EmployeeSerializer
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
    'attachment'
]

class CompanySerializer(serializers.ModelSerializer):
    """ Serialization of Company object """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    start_date = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    city = serializers.CharField(required=True, max_length=255)
    owner_id = serializers.IntegerField(required=True, write_only=True)
    employees = serializers.SerializerMethodField()
    attachment = AttachmentField(allow_null=True, required=False)

    class Meta:
        model = Company
        fields = BASE_FIELDS + [ 'employees' ]

    def get_employees(self, obj):
        """ Receives the list of employees """

        return EmployeeSerializer(obj.employees.all(),
                                         many=True, read_only=True,
                                         context={'company_id': obj.id}).data

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
