from django.core.management.base import BaseCommand
from companies.models import Specialty
from companies.index import SpecialtyIndex
from django.core.management import call_command


class Command(BaseCommand):
    """Command for importing specialties."""

    help = 'Load specialties data and indexing it'

    def handle(self, *args, **kwargs):
        """Execute command."""

        if Specialty.objects.count() == 0:
            call_command('loaddata', 'specialty.yaml')
        try:
            SpecialtyIndex.init()
        finally:
            for specialty in Specialty.objects.all():
                SpecialtyIndex.store_index(specialty)
