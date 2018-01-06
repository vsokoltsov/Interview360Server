from . import serializers, Specialty

class BaseSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = [ 'id', 'name' ]

class SpecialtySerializer(BaseSpecialtySerializer):
    """ Serializer for the specialty model """

    parent = BaseSpecialtySerializer()
    children = BaseSpecialtySerializer(many=True)

    class Meta:
        model = BaseSpecialtySerializer.Meta.model
        fields = BaseSpecialtySerializer.Meta.fields + ['children', 'parent']
