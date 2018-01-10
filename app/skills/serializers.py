from rest_framework import serializers
from .models import Skill
from .index import SkillIndex

class SkillSerializer(serializers.ModelSerializer):
    """ Serializer for Skill objects """

    class Meta:
        model = Skill
        fields = ('id', 'name', 'created_at')


    def create(self, data):
        """ Create new instance of the skill """

        skill = Skill.objects.create(**data)
        SkillIndex.store_index(skill)
        return skill

    def update(self, instance, data):
        """ Update new instance of the skill """

        instance.name = data.get('name')
        SkillIndex.store_index(instance)
        return instance
