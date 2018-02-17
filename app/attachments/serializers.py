import re
import boto
from rest_framework import serializers
from django.db import transaction
from .models import Image
from feedbacks.fields import ContentTypeField
from easy_thumbnails.files import get_thumbnailer
from app.settings import THUMBNAIL_ALIASES
import ipdb

from common.serializers.base_attachment_serializer import BaseAttachmentSerializer

class ImageSerializer(BaseAttachmentSerializer):
    """ Serializer for Image """

    content_type = ContentTypeField(required=True)
    data = serializers.FileField(write_only=True)
    object_id = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        model = Image
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
                attachment = Image.objects.create(**data)
                self._generate_thumbs(attachment)
                return attachment
        except boto.exception.S3ResponseError:
            self.errors['attachment'] = ['An error has occured']
            return False

    def _generate_thumbs(self, attachment):
        """ Generate thumbs for the attachment """

        for item in ['small_thumb', 'thumb', 'medium', 'medium_large', 'large']:
            try:
                getattr(attachment, 'image_{}'.format(item)).generate()
            except ValueError:
                pass
