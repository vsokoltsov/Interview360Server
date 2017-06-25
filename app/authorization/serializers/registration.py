from . import serializers, User
from django.db import transaction
from django_pglocks import advisory_lock

class RegistrationSerializer(serializers.ModelSerializer):

    def create(self, data):
        user = User.objects.create(
            email=data['email']
        )
        user.set_password(data['password'])

        with transaction.atomic():
            with advisory_lock('User'):
                user.save()
                return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': { 'write_only': True }}
