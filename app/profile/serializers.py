from rest_framework import serializers
from attachments.models import Attachment
from drf_writable_nested import WritableNestedModelSerializer
from authorization.serializers import UserSerializer
from .fields import AttachmentField
import ipdb

class ProfileAttachmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    attachment = AttachmentField()

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields

    def update(self, instance, data):
        """ Update existent profile """

        instance.email = data.get('email', instance.email)
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        attachment_json = data.get('attachment')

        if attachment_json:
            attachment_id = attachment_json.get('id')
            attachment = Attachment.objects.get(id=attachment_id)
            attachment.object_id=instance.id
            attachment.save()

        instance.save()

        return instance
