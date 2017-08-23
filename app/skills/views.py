from django.shortcuts import render
from rest_framework import viewsets
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class SkillsViewSet(viewsets.ModelViewSet):
    """ ViewSet for skill """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
