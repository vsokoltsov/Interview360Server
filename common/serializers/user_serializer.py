from rest_framework import serializers
from authorization.models import User
from common.serializers.base_attachment_serializer import BaseAttachmentSerializer

class UserSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'attachment')

    def get_attachment(self, obj):
        last_attachment = obj.avatars.last()
        if last_attachment:
            return BaseAttachmentSerializer(last_attachment).data
        else:
            return None
