from rest_framework import serializers
from common.serializers.specialty_serializer import BaseSpecialtySerializer


class SpecialtiesField(serializers.Field):
    """Field for the company's serializer."""

    def get_attribute(self, obj):
        """Return custom seiralizer."""

        specialties = obj.specialties.all()
        if specialties:
            return BaseSpecialtySerializer(specialties, many=True).data
        else:
            return None

    def to_representation(self, obj):
        """Return value for representation."""

        return obj

    def to_internal_value(self, data):
        """Return value how it will be represented in serializer."""

        return data
