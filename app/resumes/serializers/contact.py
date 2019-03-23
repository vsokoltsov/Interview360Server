from . import serializers, Contact, ResumesSerializer


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for contact resource."""

    resume = ResumesSerializer()

    class Meta:
        """Metaclass for serializer."""

        model = Contact
        fields = [
            'id',
            'resume',
            'email',
            'phone',
            'social_networks',
            'updated_at'
        ]
