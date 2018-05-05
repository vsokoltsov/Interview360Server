from . import serializers, Vacancy


class BaseVacancySerializer(serializers.ModelSerializer):
    """Base vacancy objects serializer."""

    company_id = serializers.SerializerMethodField()

    class Meta:
        """Metaclass for serializer."""

        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'salary',
            'company_id',
            'created_at',
            'updated_at'
        ]

    def get_company_id(self, obj):
        """Receive id of the company."""

        return obj.company.id
