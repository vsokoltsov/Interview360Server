from . import serializers
from common.serializers.user_serializer import UserSerializer


class CurrentUserSerializer(UserSerializer):
    roles = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('roles', )

    def get_roles(self, obj):
        return obj.get_roles_for_companies()
