from . import serializers, Specialty

class SpecialtiesSerializer(serializers.ModelSerializer):
    """ Specialties list serializer """

    class Meta:
        model = Specialty
        fields = [
            'id',
            'name'
        ]
