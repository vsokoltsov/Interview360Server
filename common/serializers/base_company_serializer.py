from rest_framework import serializers
from companies.models import Company
from profiles.fields import AttachmentField

class BaseCompanySerializer(serializers.ModelSerializer):
    """ Base Company Serializer class """

    attachment = AttachmentField(allow_null=True, required=False)

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'city',
            'description',
            'start_date',
            'created_at',
            'attachment'
        ]
