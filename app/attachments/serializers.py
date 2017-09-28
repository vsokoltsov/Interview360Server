from rest_framework import serializers
from .models import Attachment
from feedbacks.fields import ContentTypeField
import ipdb

class AttachmentBaseSerializer(serializers.ModelSerializer):
    """ Base attachment serializer """

    url = serializers.SerializerMethodField('get_attachment_url', read_only=True)

    class Meta:
        model = Attachment
        fields = [
            'id',
            'url'
        ]

    def get_attachment_url(self, obj):
        return obj.data.url

class AttachmentSerializer(AttachmentBaseSerializer):
    """ Serializer for Attachment """

    content_type = ContentTypeField(required=True)
    data = serializers.FileField(write_only=True)
    object_id = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        model = AttachmentBaseSerializer.Meta.model
        fields = AttachmentBaseSerializer.Meta.fields + [
            'object_id',
            'content_type',
            'data',
            'created_at'
        ]
