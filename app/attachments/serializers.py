from rest_framework import serializers
from .models import Attachment
from feedbacks.fields import ContentTypeField

class AttachmentSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField()
    class Meta:
        model = Attachment
        fields = [
            'id',
            'object_id',
            'content_type',
            'data',
            'created_at'
        ]
