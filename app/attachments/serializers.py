from rest_framework import serializers
from .models import Attachment
from feedbacks.fields import ContentTypeField
import ipdb

class AttachmentSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(required=True)
    url = serializers.SerializerMethodField('get_attachment_url', read_only=True)
    data = serializers.FileField(write_only=True)


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
        request = self.context['request']
        return request.build_absolute_uri(obj.data.url)
