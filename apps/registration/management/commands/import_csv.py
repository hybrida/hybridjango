import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.registration.models import Hybrid


# Example:
# username,first_name,last_name,graduation_year
# luigi,Luigi,Mario,2020
# mario,Mario,Mario,2020

class Command(BaseCommand):
    help = 'Import hybrids from given CSV file, file needs to have a header with username and the included fields\n' \
           'Remember that whitespace is included so "username, first_name, last_name" is invalid,\n' \
           'use "username,first_name,Last_name" instead (avoid whitespace around commas).\n'

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
