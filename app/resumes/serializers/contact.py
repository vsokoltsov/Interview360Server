from . import serializers, Contact, ResumesSerializer

class ContactSerializer(serializers.ModelSerializer):
    """ Serializer for contact resource """

    resume = ResumesSerializer()

    class Meta:
        model = Contact
        fields = [
            'id',
            'resume',
            'email',
            'phone',
            'social_networks',
            'updated_at'
        ]
