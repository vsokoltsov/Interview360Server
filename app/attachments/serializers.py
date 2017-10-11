import re
from rest_framework import serializers
from .models import Attachment
from feedbacks.fields import ContentTypeField
from easy_thumbnails.files import get_thumbnailer
from app.settings import THUMBNAIL_ALIASES

import ipdb

class AttachmentBaseSerializer(serializers.ModelSerializer):
    """ Base attachment serializer """

    id = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField('get_attachment_url', read_only=True)
    thumb_url = serializers.SerializerMethodField(read_only=True)
    small_thumb_url = serializers.SerializerMethodField(read_only=True)
    medium_url = serializers.SerializerMethodField(read_only=True)
    medium_large_url = serializers.SerializerMethodField(read_only=True)
    large_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attachment
        fields = [
            'id',
            'url',
            'thumb_url',
            'small_thumb_url',
            'medium_url',
            'medium_large_url',
            'large_url'
        ]

    def get_attachment_url(self, obj):
        return obj.data.url

    def get_thumb_url(self, obj):
        return obj.data['thumb'].url

    def get_small_thumb_url(self, obj):
        return obj.data['small_thumb'].url

    def get_medium_url(self, obj):
        return obj.data['medium'].url

    def get_medium_large_url(self, obj):
        return obj.data['medium_large'].url

    def get_large_url(self, obj):
        return obj.data['large'].url

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

    def validate_data(self, value):
        """ Validate data field """

        regexp = re.compile(r'image')
        if regexp.search(value.content_type) is None:
            raise serializers.ValidationError('Unsupported file type')
        return value

    def create(self, data):
        """ Create new attachment and creating thumb images """

        attachment = Attachment.objects.create(**data)

        for key, value in THUMBNAIL_ALIASES[''].items():
            get_thumbnailer(attachment.data).get_thumbnail(value)
        return attachment
