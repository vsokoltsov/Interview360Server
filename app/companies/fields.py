from rest_framework import serializers
from common.serializers.specialty_serializer import SpecialtySerializer

class SpecialtiesField(serializers.Field):
    """ Field for the company's serializer """

    def get_attribute(self, obj):
        specialties = obj.specialties.all()
        if specialties:
            return SpecialtySerializer(specialties, many=True).data
        else:
            return None

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data
