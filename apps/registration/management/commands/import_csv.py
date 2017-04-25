import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.registration.models import Hybrid


class Command(BaseCommand):
    help = 'Import hybrids from given CSV file, file needs to have a header line'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        asdf = options['file']
        with open(asdf, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    username = row.pop('username')
                    user, created = Hybrid.objects.get_or_create(username=username, defaults=row)
                    if not created:
                        self.stdout.write('{} already exists'.format(user))
