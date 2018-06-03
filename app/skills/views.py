from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .index import SkillIndex
from .search import SkillSearch
from rest_framework.response import Response


class SkillsViewSet(viewsets.ModelViewSet):
    """ViewSet for skill."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def destroy(self, request, pk=None):
        """Delete selected skill."""

        skill = self.get_object()
        SkillIndex.get(id=skill.id).delete()
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['get'])
    def search(self, request):
        """Search skills."""

        query = request.query_params.get('q')
        search = SkillSearch()
        results = search.find(query)
        return Response({'skills': results})
