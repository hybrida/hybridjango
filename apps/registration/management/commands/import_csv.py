import csv
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.registration.models import Hybrid


class Command(BaseCommand):
    help = 'Import hybrids from given CSV file, file needs to have a header line'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        file = options['file']
        with open(file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    username = row.pop('username')
                    user, created = Hybrid.objects.update_or_create(username=username, defaults=row)
                    if not created:
                        self.stdout.write('{} already exists, updating user'.format(user))
