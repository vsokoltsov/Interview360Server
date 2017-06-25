from . import serializers, User

class RegistrationSerializer(serializers.ModelSerializer):

    def create(self, data):
        user = User.objects.create(
            email=data['email']
        )
        user.set_password(data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': { 'write_only': True }}
