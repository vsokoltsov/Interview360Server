from rest_framework import serializers
from attachments.models import Attachment


class BaseAttachmentSerializer(serializers.Serializer):
    """Base attachment serializer."""

    id = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField(
        'get_attachment_url', read_only=True)
    thumb_url = serializers.SerializerMethodField(read_only=True)
    small_thumb_url = serializers.SerializerMethodField(read_only=True)
    medium_url = serializers.SerializerMethodField(read_only=True)
    medium_large_url = serializers.SerializerMethodField(read_only=True)
    large_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Metaclass for serializer."""

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
        """Return attachment url."""

        return obj.data.url

    def get_thumb_url(self, obj):
        """Return attachment thumb url."""

        return obj.image_thumb.url

    def get_small_thumb_url(self, obj):
        """Return attachment small thumb url."""

        return obj.image_small_thumb.url

    def get_medium_url(self, obj):
        """Return attachment medium url."""

        return obj.image_medium.url

    def get_medium_large_url(self, obj):
        """Return attachment large url."""

        return obj.image_medium_large.url

    def get_large_url(self, obj):
        """Return attachment large url."""

        return obj.image_large.url
