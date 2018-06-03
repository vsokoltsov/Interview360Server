from django.db import models
from django.db.models import Count


class CompanyManager(models.Manager):
    """Custom manager for Company model."""

    def prefetched_list(self, **kwargs):
        """Prefetch all necessary objects."""

        objects = self.prefetch_related(
            'images'
        )
        objects = (
            objects
            .annotate(Count('vacancy', distinct=True))
            .annotate(Count('employees'))
        )
        return objects

    def prefetched_detail(self, **kwargs):
        """Prefetch objects for detail representaiton of company."""

        objects = self.prefetch_related(
            'vacancy_set',
            'images',
            'employees',
            'employees__avatars',
            'vacancy_set__interviews')
        objects = (
            objects
            .annotate(Count('employees', distinct=True))
            .annotate(Count('vacancy', distinct=True))
        )
        return objects
