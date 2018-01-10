from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .index import SkillIndex
from rest_framework.response import Response

# Create your views here.
class SkillsViewSet(viewsets.ModelViewSet):
    """ ViewSet for skill """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def destroy(self, request, pk=None):
        """ Deletes selected skill """

        skill = self.get_object()
        SkillIndex.get(id=skill.id).delete()
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
