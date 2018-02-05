import re
import boto
from rest_framework import serializers
from django.db import transaction
from .models import Attachment
from feedbacks.fields import ContentTypeField
from easy_thumbnails.files import get_thumbnailer
from app.settings import THUMBNAIL_ALIASES
import ipdb

from common.serializers.base_attachment_serializer import BaseAttachmentSerializer

class AttachmentSerializer(BaseAttachmentSerializer):
    """ Serializer for Attachment """

    content_type = ContentTypeField(required=True)
    data = serializers.FileField(write_only=True)
    object_id = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        model = BaseAttachmentSerializer.Meta.model
        fields = BaseAttachmentSerializer.Meta.fields + [
            'object_id',
            'content_type',
            'data',
            'created_at'
        ]

    def validate_data(self, value):
        """ Validate data field """

        regexp = re.compile(r'image')
        if regexp.search(value.content_type) is None:
            raise serializers.ValidationError('Unsupported file type')
        return value

    def create(self, data):
        """ Create new attachment and creating thumb images """

        try:
            with transaction.atomic():
                attachment = Attachment.objects.create(**data)

                for key, value in THUMBNAIL_ALIASES[''].items():
                    get_thumbnailer(attachment.data).get_thumbnail(value)
                return attachment
        except boto.exception.S3ResponseError:
            self.errors['attachment'] = ['An error has occured']
            return False
