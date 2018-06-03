from rest_framework import serializers


class CustomField(serializers.Field):
    """Custom field class."""

    def __init__(self, **kwargs):
        """Create new Field instance.

        Save attr_name and serializer attributes.
        """

        self.attr_name = kwargs.pop('obj', None)
        self.serializer = kwargs.pop('serializer', None)
        super(CustomField, self).__init__(**kwargs)

    def get_attribute(self, obj):
        """Getter for the field."""

        try:
            related_object = getattr(obj, self.attr_name)
            if related_object:
                return self.serializer(related_object).data
            else:
                return None
        except KeyError as e:
            raise serializers.ValidationError({
                self.attr_name: 'There is no such attribute on a base model'
            })

    def to_representation(self, obj):
        """Return representation value."""

        return obj

    def to_internal_value(self, data):
        """Set value to the field."""

        try:
            instance = self.serializer.Meta.model.objects.get(id=data)
            return instance
        except AttributeError as e:
            raise serializers.ValidationError('There are no such attribute')
        except self.serializer.Meta.model.DoesNotExist as e:
            raise serializers.ValidationError(
                'Object with id {} does not exists'.format(data))
