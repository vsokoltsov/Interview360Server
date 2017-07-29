from rest_framework import serializers
from .models import Company, CompanyMember
from authorization.models import User
import ipdb

class CompanyMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyMember
        fields = [
            'id',
            'role',
            'created_at'
        ]

class CompanyEmployeeSerializer(serializers.ModelSerializer):
    companymember_set = serializers.SerializerMethodField(source='get_roles')

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'companymember_set'
        ]

    def get_roles(self, obj):
        ipdb.set_trace()

    def get_companymember_set(self, obj):
        company_id = self.context.get('company_id')
        queryset = CompanyMember.objects.filter(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(queryset, many=True, read_only=True).data

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    start_date = serializers.DateField(required=True)
    description = serializers.CharField()
    city = serializers.CharField(required=True, max_length=255)
    owner_id = serializers.IntegerField(required=True, write_only=True)
    employees = serializers.SerializerMethodField()
    # CompanyEmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'city',
            'description',
            'start_date',
            'created_at',
            'employees'
        ]

    def get_employees(self, obj):
        return CompanyEmployeeSerializer(obj.employees.all(),
                                         many=True, read_only=True,
                                         context={'company_id': obj.id}).data

    def validate_owner_id(self, value):
        try:
            self.owner = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("There is no such user")

    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id', None)
        company = Company.objects.create(**validated_data)
        # ipdb.set_trace()
        company_member = CompanyMember.objects.create(user_id=owner_id, company_id=company.id, role='owner')
        return company
