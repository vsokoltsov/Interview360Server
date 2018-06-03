from . import serializers, Resume, UserSerializer


class ResumesSerializer(serializers.ModelSerializer):
    """Resumes serializer class."""

    user = UserSerializer()

    class Meta:
        """Metaclass for serializer."""

        model = Resume
        fields = [
            'id',
            'title',
            'user',
            'salary',
            'updated_at'
        ]
