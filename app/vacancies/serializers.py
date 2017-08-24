from rest_framework import serializers
from .models import Vacancy
import ipdb

class VacancySerializer(serializers.ModelSerializer):
    """ Serializer for vacancies object """

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'salary',
            'company',
            'created_at',
            'updated_at'
        ]
