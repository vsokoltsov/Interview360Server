from . import serializers, Resume

class ResumesSerializer(serializers.ModelSerializer):
    """ Resumes serializer class """

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'user',
            'salary',
            'updated_at'
        ]
