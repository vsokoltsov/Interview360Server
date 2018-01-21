from . import serializers, Workplace, BaseCompanySerializer, ResumesSerializer

class WorkplaceSerializer(serializers.ModelSerializer):
    """ Serializer for workplace resource """

    company = BaseCompanySerializer()
    resume = ResumesSerializer()

    class Meta:
        model = Workplace
        fields = [
            'id',
            'company',
            'resume',
            'position',
            'description',
            'start_date',
            'end_date',
            'updated_at'
        ]
