from django.core.management.base import BaseCommand
from django.core.management import call_command

from common.indexes.base import init_indexes


class Command(BaseCommand):
    """Command for Initial indexes building."""

    help = 'Load specialties data and indexing it'

    def handle(self, *args, **kwargs):
        """Execute command."""

        init_indexes()
