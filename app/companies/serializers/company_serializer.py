from . import serializers, User, Company, CompanyMember
from .company_employee_serializer import CompanyEmployeeSerializer

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    start_date = serializers.DateField(required=True)
    description = serializers.CharField()
    city = serializers.CharField(required=True, max_length=255)
    owner_id = serializers.IntegerField(required=True, write_only=True)
    employees = serializers.SerializerMethodField()

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
        company_member = CompanyMember.objects.create(user_id=owner_id,
                                                      company_id=company.id,
                                                      role='owner')
        return company
