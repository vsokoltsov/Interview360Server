from . import serializers, CompanyMember, transaction
from profiles.fields import AttachmentField
from profiles.index import UserIndex
from .company_member_serializer import CompanyMemberSerializer
from common.serializers.user_serializer import UserSerializer
from attachments.models import Attachment


class EmployeeSerializer(UserSerializer):
    """Company employee serializer class."""

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    attachment = AttachmentField(required=False, allow_null=True)
    member_role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Metaclass for EmployeeSerializer."""

        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ('member_role', )
        read_only_fields = UserSerializer.Meta.fields

    def get_member_role(self, obj):
        """Get role for the employee."""

        company_id = self.context.get('company_id')
        company_member = CompanyMember.objects.get(
            user_id=obj.id, company_id=company_id
        )
        return CompanyMemberSerializer(company_member, read_only=True).data

    def update(self, instance, data):
        """Update employee's instance."""

        with transaction.atomic():
            instance.email = data.get('email', instance.email)
            instance.first_name = data.get('first_name', instance.first_name)
            instance.last_name = data.get('last_name', instance.last_name)
            attachment_json = data.get('attachment')

            if attachment_json:
                attachment_id = attachment_json.get('id')
                attachment = Attachment.objects.get(id=attachment_id)
                attachment.object_id = instance.id
                attachment.save()

            instance.save()
            UserIndex.store_index(instance)
            return instance
