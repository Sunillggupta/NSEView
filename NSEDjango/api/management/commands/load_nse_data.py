"""
Management command to load NSE data into database
"""
from django.core.management.base import BaseCommand

from NSEView.NSEDjango.api.services import sync_indices


class Command(BaseCommand):
    help = 'Load NSE indices data from API into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-history',
            action='store_true',
            help='Skip recording an IndexHistory snapshot for this sync',
        )

    def handle(self, *args, **options):
        self.stdout.write('Loading NSE data...')

        try:
            result = sync_indices(record_history=not options['no_history'])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            return

        self.stdout.write(self.style.SUCCESS(
            f"Successfully synced {result['total']} indices "
            f"({result['created']} new, {result['updated']} updated)"
        ))
