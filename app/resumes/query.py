import re

from django.db.models import Count
from resumes.models import Resume
import ipdb

class ResumesQuery:
    """ Advanced Query class for the Resume """

    VALID_ORDER_FIELDS = [
        'title',
        'salary',
        'created_at',
        'updated_at',
        'workplaces_count'
    ]

    def __init__(self, params):
        """ Constructor; Set parameters instead of default ones """

        self.params = params


    def list(self):
        """ Perform query for extracting the list of the Resume instances """

        queryset = Resume.objects.select_related('user').prefetch_related(
            'user__avatars'
        ).annotate(workplaces_count=Count('workplaces'))

        if self.order:
            queryset = queryset.order_by(self.order)
        return queryset

    @property
    def salary(self):
        """ Return salary value """

        return self.params.get('salary')

    @property
    def order(self):
        """ Retur order value """

        return order if self.is_valid_order(order) else None

    @property
    def skills(self):
        """ Return skills value """

        return self.params.get('skills')

    def is_valid_order(self, order):
        """ Return whether or not the order value is valid """

        order_template = re.compile('-')
        if order_template.match(str(order)):
            order = order[1:]
        return order in self.VALID_ORDER_FIELDS
