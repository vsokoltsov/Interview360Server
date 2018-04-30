from . import serializers, Resume, UserSerializer


class ResumesSerializer(serializers.ModelSerializer):
    """ Resumes serializer class """

    user = UserSerializer()

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'user',
            'salary',
            'updated_at'
        ]
