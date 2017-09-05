from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    """ Serializer class for Feedback mode """

    class Meta:
        model = Feedback
        fields = ('id', 'created_at')
