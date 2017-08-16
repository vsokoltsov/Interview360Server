from . import serializers, User, CompanyMember, transaction
from .company_member_serializer import CompanyMemberSerializer
from authorization.serializers import UserSerializer
from django.db.utils import IntegrityError
import ipdb

class EmployeeSerializer(UserSerializer):
    """ Company employee serializer class """

    emails = serializers.ListField(write_only=True, required=True,
        max_length=10, child=serializers.CharField()
    )
    company_id = serializers.IntegerField(write_only=True, required=True)
    roles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('emails', 'company_id', 'roles',)
        read_only_fields = UserSerializer.Meta.fields

    def get_roles(self, obj):
        """ Receiving list of Employee objects """

        company_id = self.context.get('company_id')
        queryset = CompanyMember.objects.filter(user_id=obj.id,
                                                company_id=company_id)
        return CompanyMemberSerializer(queryset, many=True, read_only=True).data

    def create(self, validated_data):
        """
        Creates a new employee if they are do not exist;
        Send invintation emails
        """

        try:
            with transaction.atomic():
                for email in validated_data['emails']:
                    user = self.find_or_create_user(email)
                return True
        except:
            return False


    def find_or_create_user(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)

        return user
