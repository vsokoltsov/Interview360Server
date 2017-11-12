from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from common.serializers.base_attachment_serializer import BaseAttachmentSerializer
import ipdb

class AttachmentField(serializers.Field):
    """ Custom field for 'attachment' attribute in request """

    def get_attribute(self, obj):
        if obj.attachments.last():
            return BaseAttachmentSerializer(obj.attachments.last()).data
        else:
            return None

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data
