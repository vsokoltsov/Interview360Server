from . import (
    render,
    viewsets,
    status,
    Response,
    IsAuthenticated,
    TokenAuthentication,
    get_object_or_404,
    ResumesSerializer,
    ResumeSerializer,
    list_route,
    Resume,
    ResumesIndex,
    ResumesSearch,
    ResumeForm,
    ResumesQuery,
    ResumesFilter,
    QueryParser,
    ResumePermissions)
import ipdb


class ResumeViewSet(viewsets.ModelViewSet):
    """ Resume views """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, ResumePermissions, )
    queryset_parser = QueryParser({
        'salary': dict,
        'skills': list,
        'order': str
    })

    def get_queryset(self):
        """ Return queryset class """

        if self.action == 'list':
            params = self.queryset_parser.parse(self.request.query_params)
            query = ResumesQuery(params)
            return query.list()
        else:
            return Resume.objects.select_related('user', 'contact').prefetch_related(
                'user__avatars', 'skills',
                'workplaces', 'workplaces__company'
            ).all()

    def get_serializer_class(self):
        """ Return specific serializer for action """

        if self.action == 'list':
            return ResumesSerializer
        else:
            return ResumeSerializer

    def create(self, request):
        """ Create a new resume """

        form = ResumeForm(obj=Resume(), params=request.data)
        if form.submit():
            serializer = ResumeSerializer(form.obj)
            return Response({'resume': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ Update existing resume """

        resume = self.get_object()
        form = ResumeForm(obj=resume, params=request.data)
        if form.submit():
            serializer = ResumeSerializer(form.obj)
            return Response({'resume': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ Deletes selected resume """

        resume = self.get_object()
        resume.delete()
        ResumesIndex.get(id=resume.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['get'])
    def search(self, request):
        """ Action for resumes search """

        query = request.query_params.get('q')
        search = ResumesSearch()
        results = search.find(query)
        return Response({'resumes': results})

    @list_route(methods=['get'])
    def filters(self, request):
        """ Receive the filter value of the resumes """

        serializer = ResumesFilter({})
        return Response({'filters': serializer.data})
