from resumes.models import Resume

class ResumesQuery:
    """ Advanced Query class for the Resume """

    def __init__(self, params=None):
        """ Constructor; Set parameters instead of default ones """

        self.order = params.get('order')
        self.salary = params.get('salary')
        self.skills = params.get('skills')

    def list(self):
        """ Perform query for extracting the list of the Resume instances """

        queryset = Resume.objects.prefetch_related(
            'user', 'user__avatars'
        )
        if self.order:
            queryset = queryset.order_by(self.order)
        return queryset
