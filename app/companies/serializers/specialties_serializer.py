from . import serializers, Specialty


class SpecialtiesSerializer(serializers.ModelSerializer):
    """Specialties list serializer."""

    class Meta:
        """Metaclass for Specialties serializer."""

        model = Specialty
        fields = [
            'id',
            'name'
        ]
