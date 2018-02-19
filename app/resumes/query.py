from django.db.models import Count
from resumes.models import Resume
import ipdb

class ResumesQuery:
    """ Advanced Query class for the Resume """

    def __init__(self, params=None):
        """ Constructor; Set parameters instead of default ones """

        self.order = params.get('order')
        self.salary = params.get('salary')
        self.skills = params.get('skills')


    def list(self):
        """ Perform query for extracting the list of the Resume instances """

        queryset = Resume.objects.select_related('user').prefetch_related(
            'user__avatars'
        ).annotate(workplaces_count=Count('workplaces'))

        if self.order:
            queryset = queryset.order_by(self.order)
        return queryset
