from rest_framework import serializers
from .models import Attachment
from feedbacks.fields import ContentTypeField
import ipdb

class AttachmentSerializer(serializers.ModelSerializer):
    """ Serializer for Attachment """

    content_type = ContentTypeField(required=True)
    url = serializers.SerializerMethodField('get_attachment_url', read_only=True)
    data = serializers.FileField(write_only=True)
    object_id = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        model = Attachment
        fields = [
            'id',
            'object_id',
            'content_type',
            'data',
            'url',
            'created_at'
        ]

    def get_attachment_url(self, obj):
        return obj.data.url
