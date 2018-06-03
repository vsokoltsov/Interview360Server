from . import serializers, User, BaseAttachmentSerializer
import ipdb


class UserSerializer(serializers.ModelSerializer):
    """Base user serializer class."""

    attachment = serializers.SerializerMethodField()

    class Meta:
        """Metaclass serializer."""

        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'attachment')

    def get_attachment(self, obj):
        """Return attachment for the user."""

        last_attachment = obj.avatars.last()
        if last_attachment:
            return BaseAttachmentSerializer(last_attachment).data
        else:
            return None
