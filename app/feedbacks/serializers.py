from rest_framework import serializers
from .models import Feedback
from .fields import ContentTypeField

class FeedbackSerializer(serializers.ModelSerializer):
    """ Serializer class for Feedback mode """

    content_type = ContentTypeField()

    class Meta:
        model = Feedback
        fields = [
            'id',
            'created_at',
            'user',
            'description',
            'object_id',
            'content_type'
        ]

    def create(self, data):
        """ creates new instance of the Feedback """
        
        feedback = Feedback.objects.create(**data)
        return feedback
