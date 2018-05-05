from . import serializers, Specialty


class BaseSpecialtySerializer(serializers.ModelSerializer):
    """Base serializer for specialty."""

    class Meta:
        """Metaclass for serializer."""

        model = Specialty
        fields = ['id', 'name']
