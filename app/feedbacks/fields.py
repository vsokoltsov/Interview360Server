from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class ContentTypeField(serializers.Field):
    """Custom field for 'content_type' attribute in request."""

    def to_representation(self, obj):
        """Return value for external usage."""

        return obj.model

    def to_internal_value(self, data):
        """Return value for internal usage."""

        if not data:
            raise serializers.ValidationError('Can\'t be blank')

        app_label, model = data.split('.')
        return ContentType.objects.get(app_label=app_label, model=model)
