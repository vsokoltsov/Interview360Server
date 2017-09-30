from . import serializers, User, AttachmentBaseSerializer
import ipdb

class UserSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'attachment')

    def get_attachment(self, obj):
        return AttachmentBaseSerializer(obj.attachments.last()).data
