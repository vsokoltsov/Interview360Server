from . import serializers
from common.serializers.user_serializer import UserSerializer


class CurrentUserSerializer(UserSerializer):
    """Serializer for the current user."""

    roles = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        """Metaclass for serializer."""

        fields = UserSerializer.Meta.fields + ('roles', )

    def get_roles(self, obj):
        """Return hash of roles for the user."""

        return obj.get_roles_for_companies()
