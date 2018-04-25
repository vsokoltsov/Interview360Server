import re
from decimal import Decimal

from django.db.models import Count
from resumes.models import Resume
from common.queries import BaseQuery, QueryOrderMixin
import ipdb

class ResumesQuery(BaseQuery, QueryOrderMixin):
    """ Advanced Query class for the Resume """

    order_fields = [
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
        if self.salary:
            queryset = queryset.filter(salary__range=[
                self.salary.get('min'), self.salary.get('max')
            ])

        if self.skills:
            queryset = queryset.prefetch_related(
                'skills'
            ).filter(skills__id__in=self.skills)

        if self.order:
            queryset = queryset.order_by(self.order)

        return queryset

    @property
    def salary(self):
        """ Return salary value """

        salary = self.params.get('salary')
        return salary if self.is_valid_salary(salary) else None

    @property
    def skills(self):
        """ Return skills value """

        skills = self.params.get('skills')
        return skills if self.is_valid_skills(skills) else None

    def is_valid_salary(self, salary):
        """ Return whether or not the salary is valid """

        try:
            Decimal(salary.get('min'))
            Decimal(salary.get('max'))
            return True
        except (AttributeError, TypeError, ValueError):
            return None

    def is_valid_skills(self, skills):
        """ Return whether or not skills are valid """

        try:
            list(skills)
            [int(item) for item in skills]
            return True
        except (TypeError, ValueError):
            return None
