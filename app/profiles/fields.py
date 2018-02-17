from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from common.serializers.base_attachment_serializer import BaseAttachmentSerializer
import ipdb

class AttachmentField(serializers.Field):
    """ Custom field for 'attachment' attribute in request """

    def get_attribute(self, obj):
        attachment = self.get_attachment(obj)
        if attachment:
            return BaseAttachmentSerializer(attachment).data
        else:
            return None

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data

    def get_attachment(self, obj):
        """ Get attachment according to the actual value """
        try:
            return obj.attachments.last()
        except AttributeError:
            return obj.avatars.last()
