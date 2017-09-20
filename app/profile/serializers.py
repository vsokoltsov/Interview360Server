from rest_framework import serializers
from authorization.serializers import UserSerializer

class ProfileSerializer(UserSerializer):
    email = serializers.EmailField(requred=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)

    def update(self, instance, data):
        """ Update existent profile """

        instance.email = data.get('email', instance.email)
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        return instance
